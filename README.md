# dbt-tidb

This repo is fork form [dbt-mysql](https://github.com/dbeatty10/dbt-mysql). We added support for [TiDB](https://en.pingcap.com/tidb/) database based on the dbt-mysql adapter. More information what you want to know about dbt-mysql can be found in dbt-mysql repository.
Here would like to focus on the TiDB adapter.

This plugin ports [dbt](https://getdbt.com) functionality to TiDB.

Table of Contents
=================

   * [Installation](#installation)
   * [Supported features](#supported-features)
   * [Profile Configuration](#profile-configuration)
   * [Database user Privileges](#database-user-privileges)
   * [Running Tests](#running-tests)

### Installation
Compile by source code.

```bash
$ git clone https://github.com/Daemonxiao/dbt-tidb.git
$ cd dbt-tidb
$ pip install .
```
TODO: Also, you can get it from pypi.

```bash
$ pip install dbt-tidb
```
### Supported features

| TiDB 5.0 | Feature                     |
|:--------:|-----------------------------|
|    ✅     | Table materialization       |
|    ✅     | View materialization        |
|    ✅     | Incremental materialization |
|    ✅     | Ephemeral materialization   |
|    ✅     | Seeds                       |
|    ✅     | Sources                     |
|    ✅     | Custom data tests           |
|    ✅     | Docs generate               |
|    ✅     | Snapshots                   |



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
      ssl_disabled: True
```

| Option          | Description                                                                         | Required? | Example                        |
| --------------- | ----------------------------------------------------------------------------------- |-----------|--------------------------------|
| type            | The specific adapter to use                                                         | Required  | `tidb`                         |
| server          | The server (hostname) to connect to                                                 | Required  | `yourorg.tidb.com`             |
| port            | The port to use                                                                     | Required  | `4000`                         |
| schema          | Specify the schema (database) to build models into                                  | Required  | `analytics`                    |
| username        | The username to use to connect to the server                                        | Required  | `dbt_admin`                    |
| password        | The password to use for authenticating to the server                                | Required  | `correct-horse-battery-staple` |
| ssl_disabled    | Set to enable or disable TLS connectivity to mysql5.x                               | Optional  | `True` or `False`              |

### Database user Privileges
Your database user would be able to have some abilities to read or write, such as `SELECT`, `CREATE` and so on.
You can find some help [here](https://github.com/dbeatty10/dbt-mysql.git) about TiDB privileges management.

| Required Privilege     |
|------------------------|
| SELECT                 |
| CREATE                 |
| CREATE TEMPORARY TABEL |
| CREATE VIEW            |
| INSERT                 |
| DROP                   |
| SHOW DATABASE          |
| SHOW VIEW              |
| SUPER                  |

### Running Tests
See [test/README.md](test/README.md) for details on running the integration tests.

