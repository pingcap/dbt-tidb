{% macro tidb__cast_bool_to_text(field) %}

    case {{ field }}
        when true then 'true'
        when false then 'false'
    end

{% endmacro %}