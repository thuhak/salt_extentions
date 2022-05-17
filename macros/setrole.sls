############################
#  set&unset grains roles  #
############################

{% macro setrole() -%}
{% set roles = salt["grains.get"]("roles", []) %}
{% for role in varargs %}
{% if role not in roles %}
{{ role }}_roles:
{% if roles == [] and loop.index == 1 %}
  grains.present:
    - force: True
    - value:
      - {{ role }}
    - name: roles
{% else %}
  grains.append:
    - value:
      - {{ role }}
    - name: roles
{% endif %}
{% endif %}
{% endfor %}
{%- endmacro %}


{% macro unsetrole() -%}
{% for role in varargs %}
unset_{{ role }}:
  grains.list_absent:
    - name: roles
    - value:
      - {{ role }}
{% endfor %}
{%- endmacro %}