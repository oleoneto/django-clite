{
  "project": {
    "name": "{{ project }}",
    "path": "{{ path }}",
    "created_at": "{{ created_at }}",
    "updated_at": "{{ updated_at }}",
  },
  "apps": [
  {% for app in apps %}
    {
        "{{ app.name }}": {
            "path": "{{ app['path'] }}",
            "models": []
        }
    },
  {% endfor %}
  ]
}