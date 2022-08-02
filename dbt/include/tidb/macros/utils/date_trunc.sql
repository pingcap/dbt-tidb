-- date_trunc can truncate date with given datepart(year,month,quarter,day is supported)
{% macro tidb__date_trunc(datepart, date) -%}

     {%- if datepart =='day' -%}

         DATE_FORMAT({{date}}, '%Y-%m-%d')

     {%- elif datepart == 'month' -%}

         DATE_FORMAT({{date}}, '%Y-%m-01')

     {%- elif datepart == 'quarter' -%}

         case QUARTER({{date}})
            when 1 then DATE_FORMAT({{date}}, '%Y-01-01')
            when 2 then DATE_FORMAT({{date}}, '%Y-04-01')
            when 2 then DATE_FORMAT({{date}}, '%Y-07-01')
            when 2 then DATE_FORMAT({{date}}, '%Y-10-01')
         end

     {%- elif datepart == 'year' -%}

         DATE_FORMAT({{date}}, '%Y-01-01')

     {%- else -%}

            {{ exceptions.raise_compiler_error("macro date_trunc not implemented for datepart ~ '" ~ datepart ~ "' ~ on TiDB") }}

     {%- endif -%}

{%- endmacro %}