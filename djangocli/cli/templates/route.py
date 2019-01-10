from jinja2 import Template


route_view = Template("""
def {{ route.lower() }}(request):
    context = {
        'active': True,
        'route': '{{ route.lower() }}',
     }
    return render(request, '{{ route.lower() }}.html', context)
""")

route__simple_template = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ route.capitalize() }}</title>
    {% if framework %}<link rel="stylesheet" href="{{ framework }}/css/{{ framework }}.css">
    <script src="{{ framework }}/js/{{ framework }}.js"></script>{% endif %}
    <link rel="stylesheet" href="static/css/main.css">
</head>
<body>
    <h1>Template for {{ route.capitalize() }}</h1>

    <script src="static/js/main.js"></script>
</body>
</html>
""")

route_template_with_framework = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ route.capitalize() }}</title>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    {% if framework %}<link rel="stylesheet" href="{{ framework[0]['link'] }}" integrity="{{ framework[0]['integrity']}}" crossorigin="anonymous">
    <script src="{{ framework[1]['src'] }}" integrity="{{ framework[0]['integrity']}}" crossorigin="anonymous"></script>{% endif %}
    <link rel="stylesheet" href="static/css/main.css">
</head>
<body>
    <h1>Template for {{ route.capitalize() }}</h1>

    <script src="static/js/main.js"></script>
</body>
</html>
""")

route_url = Template("""
urlpatterns += [
    path('{% if route == 'index' %}/{% else %}{{ route }}/{% endif %}', {{ route }}, name='{{ route }}'),
]
""")

route_path = Template("""
path('{% if route == 'index' %}/{% else %}{{ route }}/{% endif %}', {{ route }}, name='{{ route }}'),
""")
