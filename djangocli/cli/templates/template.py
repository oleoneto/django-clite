from jinja2 import Template


base_template = Template("""{{ '{% load static from staticfiles %}' }}

{{ '{% comment %}' }}
    Template for {{ name }}
    Describe the template here.
{{ '{% endcomment %}' }}

{{ '{% block header %}{% endblock header %}' }}

{{ '{% block body %}{% endblock body %}' }}

{{ '{% block footer %}{% endblock footer %}' }}

{{ '{% block scripts %}{% endblock scripts %}' }}
""")
