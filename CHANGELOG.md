# dbt-tidb changelog

## [1.2.0]2022-8-22
## Features
- Support dbt-core v1.2.0 (https://github.com/pingcap/dbt-tidb/pull/6)
- Lift + shift for cross-db macros (https://github.com/pingcap/dbt-tidb/pull/6)
- Support connection retry (https://github.com/pingcap/dbt-tidb/pull/6)
- Support grant (https://github.com/pingcap/dbt-tidb/pull/6)

## [1.0.1]2022-8-22
## Fixes
- Add quote to column in create_table_as marco (https://github.com/pingcap/dbt-tidb/pull/9)
- Delete PRI, UNI constraint in create_table_as marco (https://github.com/pingcap/dbt-tidb/pull/10)

## Enhancement
- Use black to fmt Python (https://github.com/pingcap/dbt-tidb/pull/12)

## [1.1.0]2022-8-22
## Fixes
- Add quote to column in create_table_as marco (https://github.com/pingcap/dbt-tidb/pull/9)
- Delete PRI, UNI constraint in create_table_as marco (https://github.com/pingcap/dbt-tidb/pull/10)
- Fix the inaccurate supported features in README.md (https://github.com/pingcap/dbt-tidb/pull/13)

## Enhancement
- Use black to fmt Python (https://github.com/pingcap/dbt-tidb/pull/12)
- Add test for TiDB 5.3 in GitHub action (https://github.com/pingcap/dbt-tidb/pull/13)
- Use new test framework in test suite (dbt.tests.adapter.basic) (https://github.com/pingcap/dbt-tidb/pull/13)

## Features
- Support dbt-core v1.1.0 (https://github.com/pingcap/dbt-tidb/pull/13)
- Support multiple unique key parameter in the incremental model and add tests for it (https://github.com/pingcap/dbt-tidb/pull/13)
- Support Python 3.10 and drop support for Python 3.7 (https://github.com/pingcap/dbt-tidb/pull/13)

## [1.0.0]2022-3-31
* first tidb adapter for dbt plugin
* work on TiDB>=4.0
* work on dbt-core==1.0.1
