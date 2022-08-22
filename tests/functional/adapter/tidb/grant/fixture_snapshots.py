my_snapshot_sql = """
{% snapshot my_snapshot %}
    {{ config(
        check_cols='all', unique_key='id', strategy='check',
        target_database=database, target_schema=schema
    ) }}
    select 1 as id, cast('blue' as char) as color
{% endsnapshot %}
""".strip()

snapshot_schema_yml = """
version: 2
snapshots:
  - name: my_snapshot
    config:
      grants:
        select: ["{{ env_var('DBT_TEST_USER_1') }}"]
"""

user2_snapshot_schema_yml = """
version: 2
snapshots:
  - name: my_snapshot
    config:
      grants:
        select: ["{{ env_var('DBT_TEST_USER_2') }}"]
"""
