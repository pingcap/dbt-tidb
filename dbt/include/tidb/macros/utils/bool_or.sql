{% macro tidb__bool_or(expression) -%}

    max({{ expression }})

{%- endmacro %}