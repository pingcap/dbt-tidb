-- add interval to given from_date_or_timestamp with datepart(day,month,hour...)
{% macro tidb__dateadd(datepart, interval, from_date_or_timestamp) %}

    DATE_ADD(
        {{ from_date_or_timestamp }},
        interval {{ interval }} {{ datepart }}
        )

{% endmacro %}