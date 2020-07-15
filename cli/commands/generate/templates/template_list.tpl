{% raw %}
{% load cache %}

{% comment %}
    Describe the template here.
{% endcomment %}

{% block header %}{% endblock header %}
{% block body %}
{% endraw %}
    <h2>{{ page_title }}</h2>
{% raw %}
    <ul>
    {% for object in object_list %}
    <li>
        <a href="{{ object.get_absolute_url }}">{{ object }}</a>
    </li>
    {% endfor %}
    </ul>
{% endblock body %}

{% block footer %}{% endblock footer %}

{% block scripts %}{% endblock scripts %}
{% endraw %}
