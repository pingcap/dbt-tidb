# tidb does not support cast to timestamp, so cast to datatime

models__test_dateadd_sql = """
with data as (

    select * from {{ ref('data_dateadd') }}

)

select
    case
        when datepart = 'hour' then cast({{ dateadd('hour', 'interval_length', 'from_time') }} as {{ api.Column.translate_type('DATETIME') }})
        when datepart = 'day' then cast({{ dateadd('day', 'interval_length', 'from_time') }} as {{ api.Column.translate_type('DATETIME') }})
        when datepart = 'month' then cast({{ dateadd('month', 'interval_length', 'from_time') }} as {{ api.Column.translate_type('DATETIME') }})
        when datepart = 'year' then cast({{ dateadd('year', 'interval_length', 'from_time') }} as {{ api.Column.translate_type('DATETIME') }})
        else null
    end as actual,
    result as expected

from data
"""

models__test_dateadd_yml = """
version: 2
models:
  - name: test_dateadd
    tests:
      - assert_equal:
          actual: actual
          expected: expected
"""
