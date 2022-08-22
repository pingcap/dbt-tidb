-- the behavior is a little different from default_datediff that it will round down rather than round up
-- and millisecond is not supported
{% macro tidb__datediff(first_date, second_date, datepart) -%}
    {%- if datepart =='millisecond' -%}

       {{ exceptions.raise_compiler_error("macro datediff not implemented for datepart ~ '" ~ datepart ~ "' ~ on TiDB") }}

    {%- else -%}

       TIMESTAMPDIFF({{datepart}},{{first_date}},{{second_date}})

    {%- endif -%}

{%- endmacro %}