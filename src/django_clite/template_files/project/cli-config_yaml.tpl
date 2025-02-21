project: {{ project }}
{% if apps %}apps:{% for app in apps %}
  - {{ app }}
{% endfor %}{% endif %}
