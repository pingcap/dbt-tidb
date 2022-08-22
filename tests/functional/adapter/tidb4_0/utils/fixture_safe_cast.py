seeds__data_safe_cast_csv = """field,output
abc,abc
123,123
,
"""

# tidb does not support cast to text, so cast to char
models__test_safe_cast_sql = """
with data as (
    select * from {{ ref('data_safe_cast') }}
)
select
    {{ safe_cast('field', api.Column.translate_type('char')) }} as actual,
    output as expected
from data
"""


models__test_safe_cast_yml = """
version: 2
models:
  - name: test_safe_cast
    tests:
      - assert_equal:
          actual: actual
          expected: expected
"""
