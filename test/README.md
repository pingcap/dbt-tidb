# Testing dbt-tidb

## Overview

Here are the steps to run the tests:
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

### Database parameters

* **By environment variables:** Create the following environment variables (e.g., `export {VARIABLE}={value}` in a bash shell or via a tool like [`direnv`](https://direnv.net/)):
     `DBT_TIDB_SERVER_NAME`, 
     `DBT_TIDB_SERVER_NAME`, 
     `DBT_TIDB_PASSWORD`

* **By spec file:** Modify parameters such as the `username`, `password`, and `server` in all the [configuration files](integration/tidb.dbtspec).

If you use any bash special characters in your password (like `$`), then you will need to escape them (like `DBT_TIDB_PASSWORD=pas\$word` instead of `DBT_TIDB_PASSWORD=pas$word`).

### (Optional) Docker

Here has a reference. You can also install TiDB contianer using the following command.

We need three containers with different TiDB version.

```
# tidb:nightly
docker pull pingcap/tidb:nightly
docker run -d --name tidb -p 4000:4000 pingcap/tidb:nightly
#tidb:v5.1.0
docker pull pingcap/tidb:v5.1.0
docker run -d --name tidb -p 4001:4000 pingcap/tidb:v5.1.0
#tidb:v4.0.0
docker pull pingcap/tidb:v4.0.0
docker run -d --name tidb -p 4002:4000 pingcap/tidb:v4.0.0
```



### Run tests

Run the test specs in this repository:
```
pytest -v test/integration/tidb.dbtspec && \
pytest -v test/integration/tidb_v4.0-v5.0.dbtspec && \
pytest -v test/integration/tidb_v5.1-v5.2.dbtspec
```
