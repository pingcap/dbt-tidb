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

