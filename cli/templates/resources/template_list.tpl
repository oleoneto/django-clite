{%- raw -%}
{% comment %}
    Describe the template here.
{% endcomment %}

{% block content %}
    <div class="container">
        <h2>ListView</h2>
        <div class="row">
            {% for object in object_list %}
            <div class="card">
                <div class="card-body">
                    <h3 class="card-title">
                        <a href="{{ object.get_absolute_url }}">{{ object }}</a>
                    </h3>
                </div>
                <div class="card-text"></div>
                <div class="card-footer"></div>
            </div>
            {% endfor %}
        </div>
    </div>
{% endblock %}
{%- endraw %}
