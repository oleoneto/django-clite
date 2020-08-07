{%- raw %}
{% comment %}
    Describe the template here.
{% endcomment %}

{% block content %}
    <div class="container">
        <h2 class="title">{{ object }}</h2>

        <form action="#delete" method="POST">
            {% csrf_token %}
            <h5>
                Are you sure you want to delete <a href="{{ object.get_absolute_url }}">{{ object }}</a>?
            </h5>
            <button class="btn btn-danger" type="submit" value="yes">Delete</button>
            <a href="{{ object.get_absolute_url }}" class="btn btn-primary" type="submit" value="no">Cancel</a>
        </form>
    </div>
{% endblock %}
{% endraw -%}
