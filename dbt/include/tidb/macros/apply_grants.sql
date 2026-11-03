-- support Select/Insert/Delete/Update now
{% macro default__get_show_grant_sql(relation) %}

    select case(Table_priv) when null then null else 'select' end as privilege_type, `User` as grantee from mysql.tables_priv  where `DB` = {{ adapter.sql_string_literal(relation.schema) }} and `Table_name` = {{ adapter.sql_string_literal(relation.identifier) }} and Table_priv like '%Select%'
    union ALL
    select case(Table_priv) when null then null else 'insert' end as privilege_type, `User` as grantee from mysql.tables_priv  where `DB` = {{ adapter.sql_string_literal(relation.schema) }} and `Table_name` = {{ adapter.sql_string_literal(relation.identifier) }} and Table_priv like '%Insert%'
    union ALL
    select case(Table_priv) when null then null else 'update' end as privilege_type, `User` as grantee from mysql.tables_priv  where `DB` = {{ adapter.sql_string_literal(relation.schema) }} and `Table_name` = {{ adapter.sql_string_literal(relation.identifier) }} and Table_priv like '%Update%'
    union ALL
    select case(Table_priv) when null then null else 'delete' end as privilege_type, `User` as grantee from mysql.tables_priv  where `DB` = {{ adapter.sql_string_literal(relation.schema) }} and `Table_name` = {{ adapter.sql_string_literal(relation.identifier) }} and Table_priv like '%Delete%'

{% endmacro %}

{%- macro tidb__get_grant_sql(relation, privilege, grantees) -%}
    grant {{ privilege }} on {{ relation.quote(schema=True, identifier=True) }} to {% for grantee in grantees %}{{ adapter.quote(grantee) if grantee else "''" }}{% if not loop.last %}, {% endif %}{% endfor %}
{%- endmacro -%}

 {%- macro tidb__get_revoke_sql(relation, privilege, grantees) -%}
    revoke {{ adapter.revoke_privilege_sql(privilege) }} on {{ relation.quote(schema=True, identifier=True) }} from {% for grantee in grantees %}{{ adapter.quote(grantee) if grantee else "''" }}{% if not loop.last %}, {% endif %}{% endfor %}
{%- endmacro -%}

-- tidb-dbt does not support multi=true now, so we need to split every grant/revoke statement
{% macro tidb__call_dcl_statements(dcl_statement_list) %}
    {% for dcl_statement in dcl_statement_list %}
        {% call statement('grant_or_revoke') %}
            {{ dcl_statement }}
        {% endcall %}
    {% endfor %}
{% endmacro %}
