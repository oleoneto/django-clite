[
    {% for i in range(total) -%}
    {
        "pk": {{ loop.index }},
        "model": "{{ app }}.{{ classname }}",
        "fields": {
            {% for attr_name, f in fields.items() -%}
            "{{ attr_name }}": "{{ f.example_value }}"{% if loop.index < loop.length %}, {%- endif -%}
            {% endfor %}
        }
    }{% if loop.index < loop.length %},{% endif -%}
    {% endfor %}
]
