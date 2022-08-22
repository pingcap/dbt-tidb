-- split_part will split string with given delimiter_text, and it will return the element at element
{% macro tidb__split_part(string_text, delimiter_text, part_number) %}


  {% if part_number >= 0 %}

      SUBSTRING_INDEX(SUBSTRING_INDEX({{ string_text }}, {{ delimiter_text }}, {{ part_number }}), {{ delimiter_text }}, -1)

  {% else %}

      SUBSTRING_INDEX(SUBSTRING_INDEX({{ string_text }}, {{ delimiter_text }}, {{ part_number }}), {{ delimiter_text }}, 1)

  {% endif %}


{% endmacro %}