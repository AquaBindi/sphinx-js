.. js:data:: {{ name }}

   {% if description -%}
     {{ description|indent(3) }}
   {%- endif %}

   {% for heads, tail in fields -%}
     :{{ heads|join(' ') }}: {{ tail }}
   {% endfor %}

   {{ content|indent(3) }}
