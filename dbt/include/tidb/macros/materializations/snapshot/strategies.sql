
{% macro tidb__snapshot_hash_arguments(args) -%}
    md5(concat_ws('|', {%- for arg in args -%}
        coalesce(cast({{ arg }} as char), '')
        {% if not loop.last %}, {% endif %}
    {%- endfor -%}))
{%- endmacro %}

-- copy from dbt-core v1.2, just alter database=None in adapter.get_relation
{% macro snapshot_check_all_get_existing_columns(node, target_exists, check_cols_config) -%}
    {%- if not target_exists -%}
        {#-- no table yet -> return whatever the query does --#}
        {{ return((false, query_columns)) }}
    {%- endif -%}

    {#-- handle any schema changes --#}
    {%- set target_relation = adapter.get_relation(database=None, schema=node.schema, identifier=node.alias) -%}

    {% if check_cols_config == 'all' %}
        {%- set query_columns = get_columns_in_query(node['compiled_sql']) -%}

    {% elif check_cols_config is iterable and (check_cols_config | length) > 0 %}
        {#-- query for proper casing/quoting, to support comparison below --#}
        {%- set select_check_cols_from_target -%}
            select {{ check_cols_config | join(', ') }} from ({{ node['compiled_sql'] }}) subq
        {%- endset -%}
        {% set query_columns = get_columns_in_query(select_check_cols_from_target) %}

    {% else %}
        {% do exceptions.raise_compiler_error("Invalid value for 'check_cols': " ~ check_cols_config) %}
    {% endif %}

    {%- set existing_cols = adapter.get_columns_in_relation(target_relation) | map(attribute = 'name') | list -%}
    {%- set ns = namespace() -%} {#-- handle for-loop scoping with a namespace --#}
    {%- set ns.column_added = false -%}

    {%- set intersection = [] -%}
    {%- for col in query_columns -%}
        {%- if col in existing_cols -%}
            {%- do intersection.append(adapter.quote(col)) -%}
        {%- else -%}
            {% set ns.column_added = true %}
         {%- endif -%}
    {%- endfor -%}
    {{ return((ns.column_added, intersection)) }}
{%- endmacro %}
