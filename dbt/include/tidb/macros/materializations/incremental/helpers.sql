{% macro tidb__get_incremental_default_sql(arg_dict) %}
    {% if arg_dict["unique_key"] %}
        {% do return(get_incremental_delete_insert_sql(arg_dict)) %}
    {% else %}
        {% do return(get_incremental_append_sql(arg_dict)) %}
    {% endif %}
{% endmacro %}

{% macro get_incremental_delete_insert_sql(arg_dict) %}
    {% set target_relation = arg_dict["target_relation"] %}
    {% set tmp_relation = arg_dict["temp_relation"] %}
    {% set unique_key = arg_dict["unique_key"] %}
    {% set dest_columns = arg_dict["dest_columns"] %}
    --  use get_delete_insert_merge_sql after support multi sql
    --  we will delete then insert now
    {% set build_sql = incremental_delete(target_relation, tmp_relation, unique_key, dest_columns) %}
    {% call statement("pre_main") %}
        {{ build_sql }}
    {% endcall %}
    {% do return(incremental_insert(target_relation, tmp_relation, unique_key, dest_columns)) %}
{% endmacro %}

{% macro get_incremental_append_sql(arg_dict) %}
    {% set target_relation = arg_dict["target_relation"] %}
    {% set tmp_relation = arg_dict["temp_relation"] %}
    {% set unique_key = arg_dict["unique_key"] %}
    {% set dest_columns = arg_dict["dest_columns"] %}
    {% do return(incremental_insert(target_relation, tmp_relation, unique_key, dest_columns)) %}
{% endmacro %}

-- need to support unique_key is sequence
{% macro incremental_delete(target, source, unique_key, dest_columns) %}

    {% if unique_key %}
        {% if unique_key is sequence and unique_key is not string %}
            delete from {{ target }}
            where (
            {% for key in unique_key %}
                {{ key }} in (select {{ key }} from {{ source }})
                {{ "and " if not loop.last }}
            {% endfor %}
            );
        {% else %}
            delete from {{ target }}
            where (
            {{ unique_key }}) in (
            select ({{ unique_key }})
            from {{ source }}
            );

        {% endif %}
    {% endif %}

{%- endmacro %}

{% macro incremental_insert(target, source, unique_key, dest_columns) %}

    {%- set dest_cols_csv = get_quoted_csv(dest_columns | map(attribute="name")) -%}

    insert into {{ target }} ({{ dest_cols_csv }})
    (
       select {{ dest_cols_csv }}
       from {{ source }}
    )

{%- endmacro %}

-- don't use it because dbt-tidb does not support multi sql
{% macro tidb__get_delete_insert_merge_sql(target, source, unique_key, dest_columns) -%}

    {%- set dest_cols_csv = get_quoted_csv(dest_columns | map(attribute="name")) -%}

    {% if unique_key %}
        {% if unique_key is sequence and unique_key is not string %}
            delete from {{ target }}
            where (
                {% for key in unique_key %}
                    {{ key }} in (select {{ key }} from {{ source }})
                    {{ "and " if not loop.last }}
                {% endfor %}
            );
        {% else %}
            delete from {{ target }}
            where (
                {{ unique_key }}) in (
                select ({{ unique_key }})
                from {{ source }}
            );

        {% endif %}
    {% endif %}

    insert into {{ target }} ({{ dest_cols_csv }})
    (
       select {{ dest_cols_csv }}
       from {{ source }}
    )

{%- endmacro %}

