{%- raw %}
{% comment %}
    Describe the template here.
{% endcomment %}

{% block content %}
    <div class="container">
        <h2 class="title">{{ object }}</h2>

        <div id="modelForm">
            {{ form }}
        </div>
    </div>
{% endblock %}
{% endraw -%}
