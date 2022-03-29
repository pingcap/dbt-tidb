# Testing dbt-tidb

## Overview

Here are the steps to run the integration tests:
1. Set environment variables
1. Run Docker containers (optional)
1. Run tests

## Simple example

Assuming the applicable `pytest-dbt-adapter` package is installed and environment variables are set:
```bash
export DBT_TIDB_SERVER_NAME=tidb-server
export DBT_TIDB_SERVER_NAME=user_name
export DBT_TIDB_PASSWORD=password

pytest test/tidb.dbtspec
```

## Full example

### Prerequisites
- [`pytest-dbt-adapter`](https://github.com/dbt-labs/dbt-adapter-tests) package

### Environment variables

Create the following environment variables (e.g., `export {VARIABLE}={value}` in a bash shell or via a tool like [`direnv`](https://direnv.net/)):
    * `DBT_TIDB_SERVER_NAME`
    * `DBT_TIDB_SERVER_NAME`
    * `DBT_TIDB_PASSWORD`

### (Optional) Docker
Here has a reference. You can also install TiDB contianer using the following command.

```
docker pull pingcap/tidb:nightly
docker run -d --name tidb -p 4000:4000 pingcap/tidb:nightly
mysql -u root -P 4000 -h 127.0.0.1
```

If you use any bash special characters in your password (like `$`), then you will need to escape them (like `DBT_MYSQL_PASSWORD=pas\$word` instead of `DBT_MYSQL_PASSWORD=pas$word`).


### Run tests

Run the test specs in this repository:
```
pytest -v test/integration/tidb.dbtspec
```
