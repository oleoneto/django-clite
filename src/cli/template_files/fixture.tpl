[
    {% for i in range(total) -%}
    {
        "pk": {{ loop.index }},
        "model": "{{ app }}.{{ classname }}",
        "fields": {
            {% for f in fields -%}
            "{{ f.name }}": {{ f.example_value }},
            {% endfor %}
        }
    }{% if loop.index == loop.length %}{% else %},{% endif %}
    {% endfor %}
]
