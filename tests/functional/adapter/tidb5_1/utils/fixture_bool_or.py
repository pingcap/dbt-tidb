# key is the keyword in tidb,so use `key` rather than key in models__test_bool_or_sql

models__test_bool_or_sql = """
with data as (
    select * from {{ ref('data_bool_or') }}
),
data_output as (
    select * from {{ ref('data_bool_or_expected') }}
),
calculate as (
    select
        `key`,
        {{ bool_or('val1 = val2') }} as value
    from data
    group by `key`
)
select
    calculate.value as actual,
    data_output.value as expected
from calculate
left join data_output
on calculate.key = data_output.key
"""


models__test_bool_or_yml = """
version: 2
models:
  - name: test_bool_or
    tests:
      - assert_equal:
          actual: actual
          expected: expected
"""
