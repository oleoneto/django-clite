{% raw %}
{% load cache %}
{% load widget_tweaks %}

{% comment %}
    Describe the template here.
{% endcomment %}

{% block header %}{% endblock header %}
{% block body %}
    <h2>
        <a href="{{ object.course.get_absolute_url }}">{{ object }}</a>
    </h2>
    <ul>
        # for field in object.
    </ul>
{% endblock body %}

{% block footer %}{% endblock footer %}

{% block scripts %}{% endblock scripts %}
{% endraw %}
