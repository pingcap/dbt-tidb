{% macro tidb__dateadd(datepart, interval, from_date_or_timestamp) %}

    DATE_ADD(
        {{ from_date_or_timestamp }},
        interval {{ interval }} {{ datepart }}
        )

{% endmacro %}