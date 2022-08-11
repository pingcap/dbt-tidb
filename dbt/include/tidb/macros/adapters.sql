
{% macro tidb__list_schemas(database) %}
    {% call statement('list_schemas', fetch_result=True, auto_begin=False) -%}
        select distinct schema_name
        from information_schema.schemata
    {%- endcall %}

    {{ return(load_result('list_schemas').table) }}
{% endmacro %}

{% macro tidb__create_schema(relation) -%}
  {%- call statement('create_schema') -%}
    create schema if not exists {{ relation.without_identifier() }}
  {%- endcall -%}
{% endmacro %}

{% macro tidb__drop_schema(relation) -%}
  {%- call statement('drop_schema') -%}
    drop schema if exists {{ relation.without_identifier() }}
  {% endcall %}
{% endmacro %}

{% macro tidb__drop_relation(relation) -%}
    {% call statement('drop_relation', auto_begin=False) -%}
        drop {{ relation.type }} if exists {{ relation }}
    {%- endcall %}
{% endmacro %}

{% macro tidb__truncate_relation(relation) -%}
    {% call statement('truncate_relation') -%}
      truncate table {{ relation }}
    {%- endcall %}
{% endmacro %}

{% macro tidb__create_table_as(temporary, relation, sql) -%}
    {# 1. create view #}
    {% set temp_view = "temp_view" %}
    {% call statement('create_view_as') %}
        {%- set sql_header = config.get('sql_header', none) -%}
        {{ sql_header if sql_header is not none }}

        create view
            {{ relation.schema }}.{{ temp_view }}
        as (
            {{ sql }}
        )
    {% endcall %}

    {# 2. create table #}
    {% call statement('get_columns_in_relation', fetch_result=True) %}
        show columns from {{ relation.schema }}.{{ temp_view }}
    {% endcall %}

    {% set table = load_result('get_columns_in_relation').table %}

    {% call statement ('xxx') %}
        create  {% if temporary: -%}temporary{%- endif %} table if not exists
        {{ relation.include(database=False) }}
        (
            {% for row in table %}
                `{{ row[0] }}`
                {{ row[1] }}
                {% if row[2] == "NO" %} not null {% endif %}
                {% if row[3] == "PRI" %} primary key {% endif %}
                {% if row[3] == "UNI" %} unique {% endif %}
                {% if not loop.last %},{% endif %}
            {% endfor %}
        )
    {% endcall %}

    {# 3. copy data from view to table #}
    {% call statement ('cpoy_data_from_view_to_table') %}
        insert into {{ relation.include(database=False) }} select * from {{ relation.schema }}.{{ temp_view }}
    {% endcall %}

    {# 4. drop view #}
    {% call statement('drop_view') %}
        drop view if exists {{ relation.schema }}.{{ temp_view }}
    {% endcall %}

{% endmacro %}

{% macro tidb__current_timestamp() -%}
  current_timestamp()
{%- endmacro %}

{% macro tidb__rename_relation(from_relation, to_relation) -%}
  {#
    tidb rename fails when the relation already exists, so a 2-step process is needed:
    1. Drop the existing relation
    2. Rename the new relation to existing relation
  #}
  {% call statement('drop_relation') %}
    drop {{ to_relation.type }} if exists {{ to_relation }} cascade
  {% endcall %}
  {% call statement('rename_relation') %}
    rename table {{ from_relation }} to {{ to_relation }}
  {% endcall %}
{% endmacro %}

{% macro tidb__check_schema_exists(database, schema) -%}
    {# no-op #}
    {# see tidbAdapter.check_schema_exists() #}
{% endmacro %}

{% macro tidb__get_columns_in_relation(relation) -%}
    {% call statement('get_columns_in_relation', fetch_result=True) %}
        show columns from {{ relation.schema }}.{{ relation.identifier }}
    {% endcall %}

    {% set table = load_result('get_columns_in_relation').table %}
    {{ return(sql_convert_columns_in_relation(table)) }}
{% endmacro %}

{% macro tidb__list_relations_without_caching(schema_relation) %}
  {% call statement('list_relations_without_caching', fetch_result=True) -%}
    select
      null as "database",
      table_name as name,
      table_schema as "schema",
      case when table_type = 'BASE TABLE' then 'table'
           when table_type = 'VIEW' then 'view'
           else table_type
      end as table_type
    from information_schema.tables
    where table_schema = '{{ schema_relation.schema }}'
  {% endcall %}
  {{ return(load_result('list_relations_without_caching').table) }}
{% endmacro %}

{% macro tidb__generate_database_name(custom_database_name=none, node=none) -%}
  {% do return(None) %}
{%- endmacro %}
