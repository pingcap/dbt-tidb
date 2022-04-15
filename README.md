# dbt-tidb

![PyPI](https://img.shields.io/pypi/v/dbt-tidb)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dbt-tidb)
![PyPI - Downloads](https://img.shields.io/pypi/dw/dbt-tidb)
[![Integration Test](https://github.com/pingcap/dbt-tidb/actions/workflows/main.yml/badge.svg)](https://github.com/pingcap/dbt-tidb/actions/workflows/main.yml)

The `dbt-tidb` package contains all of the code enabling [dbt](https://getdbt.com) to work with 
[TiDB](https://en.pingcap.com/tidb/).

This repository is based on [dbt-mysql](https://github.com/dbeatty10/dbt-mysql).
Thanks to them for their excellent work.

## Table of Contents
 * [Installation](#installation)
 * [Supported features](#supported-features)
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

|    TiDB 4.X    | TiDB 5.0 ~ 5.2 |   TiDB >= 5.3    |            Feature             |
|:--------------:|:--------------:|:----------------:|:------------------------------:|
|       ✅        |       ✅       |        ✅        |     Table materialization      |
|       ✅        |       ✅       |        ✅        |      View materialization      |
|       ✅        |       ✅       |        ✅        |  Incremental materialization   |
|       ❌        |       ❌       |        ✅        |   Ephemeral materialization    |
|       ✅        |       ✅       |        ✅        |             Seeds              |
|       ✅        |       ✅       |        ✅        |            Sources             |
|       ✅        |       ✅       |        ✅        |       Custom data tests        |
|       ✅        |       ✅       |        ✅        |         Docs generate          |
|       ❌        |       ❌       |        ✅        |           Snapshots            |

Note: 

* TiDB 4.0 ~ 5.0 does not support [CTE](https://docs.pingcap.com/tidb/dev/sql-statement-with), 
  you should avoid using `WITH` in your SQL code.
* TiDB 4.0 ~ 5.2 does not support creating a [temporary table or view](https://docs.pingcap.com/tidb/v5.2/sql-statement-create-table#:~:text=sec\)-,MySQL%20compatibility,-TiDB%20does%20not).
* TiDB 4.X does not support using SQL func in `CREATE VIEW`, avoid it in your SQL code. 
  You can find more detail [here](https://github.com/pingcap/tidb/pull/27252).

### Profile Configuration

TiDB targets should be set up using the following configuration in your `profiles.yml` file.

**Example entry for profiles.yml:**

```
your_profile_name:
  target: dev
  outputs:
    dev:
      type: tidb
      server: 127.0.0.1
      port: 4000
      schema: database_name
      username: tidb_username
      password: tidb_password
```

| Option          | Description                                            | Required? | Example                        |
| --------------- | ------------------------------------------------------ |-----------|--------------------------------|
| type            | The specific adapter to use                            | Required  | `tidb`                         |
| server          | The server (hostname) to connect to                    | Required  | `yourorg.tidb.com`             |
| port            | The port to use                                        | Required  | `4000`                         |
| schema          | Specify the schema (database) to build models into     | Required  | `analytics`                    |
| username        | The username to use to connect to the server           | Required  | `dbt_admin`                    |
| password        | The password to use for authenticating to the server   | Required  | `correct-horse-battery-staple` |

### Database User Privileges

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

### Running Tests

See [test/README.md](test/README.md) for details on running the integration tests.

### Example

Click [here](https://github.com/pingcap/dbt-tidb/wiki/Primer-Tutorial-%7C-How-to-use-dbt-with-TiDB) to see a simple example about using dbt with dbt-tidb.

### Contributing

Welcome to contribute for dbt-tidb. See [Contributing Guide](CONTRIBUTING.md) for more information.
