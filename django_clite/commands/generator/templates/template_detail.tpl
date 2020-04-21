{% raw %}
{% load cache %}

{% comment %}
    Describe the template here.
{% endcomment %}

{% block header %}{% endblock header %}
{% block body %}
    <h2>
        <a href="{{ object.course.get_absolute_url }}">{{ object }}</a>
    </h2>
    <ul>
        {% for field in object._meta.get_fields() %}
        <li>{{ field.name }}</li>
        {% endfor %}
    </ul>
{% endblock body %}

{% block footer %}{% endblock footer %}

{% block scripts %}{% endblock scripts %}
{% endraw %}
