{%- raw -%}
{% comment %}
    Describe the template here.
{% endcomment %}

{% block content %}
    <div class="">
        <h2>ListView</h2>
        <div class="">
            {% for object in object_list %}
            <div class="card">
                <div class="body">
                    <h3 class="title">
                        <a href="{{ object.get_absolute_url }}">{{ object }}</a>
                    </h3>
                </div>
                <div class="text"></div>
                <div class="footer"></div>
            </div>
            {% endfor %}
        </div>
    </div>
{% endblock %}
{%- endraw %}
