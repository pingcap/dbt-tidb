-- bool_or is an agg function which will return true once any expression is true
-- use max to replace it
{% macro tidb__bool_or(expression) -%}

    max({{ expression }})

{%- endmacro %}