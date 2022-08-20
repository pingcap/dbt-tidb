# Testing dbt-tidb

## Overview

Here are the steps to run the tests:
1. Set up
2. Set environment variables
3. Run TiDB
4. Run tests

## Set up

Make sure you have python environment, you can find the supported python version in setup.py.
```bash
pip3 install -r requirements_dev.txt
pip3 install .
```

## Set environment variables

If you don't set environment variables, the default value will be used.
```bash
export TIDB_TEST_HOST=tidb_server # default '127.0.0.1'
export TIDB_TEST_USER=user_name # default 'root'
export TIDB_TEST_PASSWORD=password # default ''
export TIDB_TEST_PORT=port # default 4000
```

You can also change the default value in `conftest.py`.

## Run TiDB

You can run TiDB with docker, here is a reference:

```
# tidb:nightly
docker pull pingcap/tidb:nightly
docker run -d --name tidb -p 4000:4000 pingcap/tidb:nightly
# tidb:v5.1.0
docker pull pingcap/tidb:v5.1.0
docker run -d --name tidb -p 4000:4000 pingcap/tidb:v5.1.0
# tidb:v4.0.0
docker pull pingcap/tidb:v4.0.0
docker run -d --name tidb -p 4000:4000 pingcap/tidb:v4.0.0
```

You can also install tidb with [TiUP playground](https://docs.pingcap.com/tidb/stable/tiup-playground) or other way.
```
tiup playground ${version}
```

## Use pytest to test

If you specify a package, all Python files under the package will be tested. Don't forget to configure PYTHONPATH:
```
# basic
PYTHONPATH=. pytest tests/functional/adapter/tidb/basic
# utils
PYTHONPATH=. pytest tests/functional/adapter/tidb/utils
```

## Test grant

When you test grant, you need to [create three users](https://docs.pingcap.com/tidb/stable/basic-sql-operations#create-authorize-and-delete-a-user) in TiDB and set environment variables like:
```
export DBT_TEST_USER_1=user1
export DBT_TEST_USER_2=user2
export DBT_TEST_USER_3=user3
```
Then test grant:
```
PYTHONPATH=. pytest tests/functional/adapter/tidb/grant
```

## Test other versions of TiDB

> Make sure you have installed the corresponding TiDB Version

We need to test for TiDB 4.0-5.0 and TiDB 5.1-5.2 for they are partly incompatible with the latest TiDB.

They are put into the `tests/functional/adapter/tidb4_0` and `tests/functional/adapter/tidb5_0` path.

The way to test them is the same as above.
