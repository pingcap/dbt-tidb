<p align="center">
  <img src="https://github.com/pingcap/tidb/blob/21847fe58b51807696debf0f7650af948f2aa3e2/docs/logo_with_text.png" alt="TiDB logo" />
  <img src="https://raw.githubusercontent.com/dbt-labs/dbt/ec7dee39f793aa4f7dd3dae37282cc87664813e4/etc/dbt-logo-full.svg" alt="dbt logo" width="250"/>
</p>

# dbt-tidb

![PyPI](https://img.shields.io/pypi/v/dbt-tidb)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dbt-tidb)
![PyPI - Downloads](https://img.shields.io/pypi/dw/dbt-tidb)
[![Integration Test](https://github.com/pingcap/dbt-tidb/actions/workflows/main.yml/badge.svg)](https://github.com/pingcap/dbt-tidb/actions/workflows/main.yml)

The `dbt-tidb` package contains all of the code enabling [dbt](https://getdbt.com) to work with 
[TiDB](https://en.pingcap.com/tidb/).

This repository is partly based on [dbt-mysql](https://github.com/dbeatty10/dbt-mysql).
Thanks to them for their excellent work.

## Table of Contents
 * [Installation](#installation)
 * [Supported features](#supported-features)
 * [Supported functions](#supported-functions)
 * [Profile Configuration](#profile-configuration)
 * [Database User Privileges](#database-user-privileges)
 * [Running Tests](#running-tests)
 * [Example](#example)
 * [Contributing](#contributing)

## Installation
Compile by source code.

```bash
$ git clone https://github.com/pingcap/dbt-tidb.git
$ cd dbt-tidb
$ pip install .
```
Also, you can get it from pypi.

```bash
$ pip install dbt-tidb
```
## Supported features

|    TiDB 4.X    | TiDB 5.0 ~ 5.2 |   TiDB >= 5.3    |           Feature           |
|:--------------:|:--------------:|:----------------:|:---------------------------:|
|       ✅        |       ✅       |        ✅        |    Table materialization    |
|       ✅        |       ✅       |        ✅        |    View materialization     |
|       ❌        |       ❌       |        ✅        | Incremental materialization |
|       ❌        |       ✅       |        ✅        |  Ephemeral materialization  |
|       ✅        |       ✅       |        ✅        |            Seeds            |
|       ✅        |       ✅       |        ✅        |           Sources           |
|       ✅        |       ✅       |        ✅        |      Custom data tests      |
|       ✅        |       ✅       |        ✅        |        Docs generate        |
|       ❌        |       ❌       |        ✅        |          Snapshots          |
|       ✅        |       ✅       |        ✅        |      Connection retry       |
|       ✅        |       ✅       |        ✅        |            Grant            |

Note: 

* TiDB 4.0 ~ 5.0 does not support [CTE](https://docs.pingcap.com/tidb/dev/sql-statement-with), 
  you should avoid using `WITH` in your SQL code.
* TiDB 4.0 ~ 5.2 does not support creating a [temporary table or view](https://docs.pingcap.com/tidb/v5.2/sql-statement-create-table#:~:text=sec\)-,MySQL%20compatibility,-TiDB%20does%20not).
* TiDB 4.X does not support using SQL func in `CREATE VIEW`, avoid it in your SQL code. 
  You can find more detail [here](https://github.com/pingcap/tidb/pull/27252).

## Supported functions

cross-db macros are moved from dbt-utils into dbt-core, so you can use the following functions directly, see [dbt-util](https://github.com/dbt-labs/dbt-utils) on how to use them.
- bool_or
- cast_bool_to_text
- dateadd
- datediff
- date_trunc
- hash
- safe_cast
- split_part
- last_day
- cast_bool_to_text
- concat
- escape_single_quotes
- except
- intersect
- length
- position
- replace
- right
- listagg (not support yet)

> pay attention that datediff is a little different from dbt-util that it will round down rather than round up.

## Profile Configuration

TiDB targets should be set up using the following configuration in your `profiles.yml` file.

**Example entry for profiles.yml:**

```
your_profile_name:
  target: dev
  outputs:
    dev:
      type: tidb
      server: tidb.example.com
      port: 4000
      schema: database_name
      username: tidb_username
      password: tidb_password
      retries: 2
      # ssl_ca: /path/to/ca.pem  # if a custom CA is needed
```

| Option           | Description                                           | Required? | Example                        |
|------------------|-------------------------------------------------------|-----------|--------------------------------|
| type             | The specific adapter to use                           | Required  | `tidb`                         |
| server           | The server (hostname) to connect to                   | Required  | `yourorg.tidb.com`             |
| port             | The port to use                                       | Required  | `4000`                         |
| schema           | Specify the schema (database) to build models into    | Required  | `analytics`                    |
| username         | The username to use to connect to the server          | Required  | `dbt_admin`                    |
| password         | The password to use for authenticating to the server  | Required  | `correct-horse-battery-staple` |
| retries          | The retry times for connection to TiDB (1 in default) | Optional  | `2`                            |
| ssl_ca | Path to the trusted CA certificate in PEM format | Optional | `/path/to/ca.pem` |
| ssl_cert | Path to the client certificate in PEM format | Optional | `/path/to/client-cert.pem` |
| ssl_key | Path to the client private key in PEM format | Optional | `/path/to/client-key.pem` |
| ssl_verify_cert | Verify the server certificate (default: true) | Optional | `true` |
| ssl_verify_identity | Verify the server hostname (default: true) | Optional | `true` |

Connections require TLS with certificate and hostname verification by default.
The `server` hostname must match the certificate. Set `ssl_ca` if the server's
CA is not trusted by the system. Existing profiles using plaintext, self-signed
certificates, or a mismatched hostname will now fail until configured correctly.
For a trusted local development server without TLS, explicitly set both
`ssl_verify_cert: false` and `ssl_verify_identity: false`. This weakens server
authentication and allows fallback to plaintext.
Client-side `LOAD DATA LOCAL INFILE` is disabled for all connections.

When creating tables from query results, the adapter validates column types
returned by TiDB. Unsupported type declarations, including `ENUM` or `SET`
members containing backslashes, fail with an error rather than being inserted
into SQL. This validation does not change existing tables.

Table materializations use uniquely named staging views for column metadata.
Failed runs can leave `__dbt_stage_` views behind; remove abandoned views only
after confirming their builds are no longer running. Use separate schemas and
database privileges to isolate tenants: a staging view is visible to other
principals with access to its schema.

## Database User Privileges

The `grants` config supports only `SELECT`, `INSERT`, `UPDATE`, and `DELETE`
(case insensitive). Other privilege values fail before DCL execution. Grantees
are quoted as individual user names; SQL fragments and `user@host` account
expressions are not interpreted.

Your database user would be able to have some abilities to read or write, such as `SELECT`, `CREATE`, and so on.
You can find some help [here](https://docs.pingcap.com/tidb/v4.0/privilege-management) with TiDB privileges management.

| Required Privilege     |
|------------------------|
| SELECT                 |
| CREATE                 |
| CREATE TEMPORARY TABLE |
| CREATE VIEW            |
| INSERT                 |
| DROP                   |
| SHOW DATABASE          |
| SHOW VIEW              |
| SUPER                  |

## Running Tests

See [tests/README.md](tests/README.md) for details on running the integration tests.

## Example

Click [here](https://github.com/pingcap/dbt-tidb/wiki/Primer-Tutorial-%7C-How-to-use-dbt-with-TiDB) to see a simple example about using dbt with dbt-tidb.

## Contributing

Welcome to contribute for dbt-tidb. See [Contributing Guide](CONTRIBUTING.md) for more information.
