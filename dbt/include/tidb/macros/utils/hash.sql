{% macro tidb__hash(field) -%}

    md5(cast({{ field }} as CHAR))

{%- endmacro %}