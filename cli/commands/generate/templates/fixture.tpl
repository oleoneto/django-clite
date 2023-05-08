[
    {% for i in range(total) -%}
    {
        "pk": {{ loop.index }},
        "model": "{{ app }}.{{ classname }}",
        "fields": {
            {% for field in fields -%}
            {{ field }}
            {% endfor %}
        }
    }{% if loop.index == loop.length %}{% else %},{% endif %}
    {% endfor %}
]