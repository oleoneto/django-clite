from jinja2 import Template as JTemplate
import inflect


p = inflect.engine()


attribute_template = JTemplate("""{{ name }} = models.{{ type }}({{ options }})""")


model_simple_template = JTemplate("""
class {{ model | capitalize }}(models.Model):
    {% for attribute in attributes %}{{ attribute }}
    {% endfor %}
""")

model_template = JTemplate("""
class {{ model | capitalize }}(models.Model):
    {% for attribute in attributes %}{{ attribute }}
    {% endfor %}
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        db_table = '{{ model | capitalize }}_table'
        ordering = ['-created_at']
        {% if abstract %}abstract = True{% endif %}
    
    def __str__(self):
        return {% if descriptor %}self.{{ descriptor }}{% else %}None{% endif %}
""")


model_admin_template = JTemplate("""
class {{ model | capitalize }}Admin(admin.ModelAdmin):
    pass
admin.site.register({{ model | capitalize }}, {{model}}Admin)
""")


route_template = JTemplate("""
def {{ route | lower }}(request):
    context = {
        active: True,
        route: '{{ route | lower }}',
     }
    return render(request, '{{ route | lower }}.html', context)
""")


form_template = JTemplate("""
class {{ model | capitalize }}Form(forms.Form):
    class Meta:
        model = {{ model | capitalize }}
        fields = "__all__"
""")


serializer_template = JTemplate("""
class {{ model | capitalize }}Serializer(serializers.ModelSerializer):
    # If model has foreign key to another model, add it like so:
    # models = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = {{ model | capitalize }}
        fields = "__all__"
""")

viewset_template = JTemplate("""
class {{ model | capitalize }}Viewset(viewsets.{% if read_only %}ReadOnlyModelViewSet{% else %}ModelViewSet{% endif %}):
    queryset = {{ model }}.objects.all()
    serializer_class = {{ model | capitalize }}Serializer
""")

html__simple_template = JTemplate("""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ route | capitalize }}</title>
    {% if framework %}<link rel="stylesheet" href="{{ framework }}/css/{{ framework }}.css">
    <script src="{{ framework }}/js/{{ framework }}.js"></script>{% endif %}
    <link rel="stylesheet" href="static/css/main.css">
</head>
<body>
    <h1>Template for {{ route | capitalize }}</h1>
    
    <script src="static/js/main.js"></script>
</body>
</html>
""")

html_template = JTemplate("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ route | capitalize }}</title>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    {% if framework %}<link rel="stylesheet" href="{{ framework[0]['link'] }}" integrity="{{ framework[0]['integrity']}}" crossorigin="anonymous">
    <script src="{{ framework[1]['src'] }}" integrity="{{ framework[0]['integrity']}}" crossorigin="anonymous"></script>{% endif %}
    <link rel="stylesheet" href="static/css/main.css">
</head>
<body>
    <h1>Template for {{ route | capitalize }}</h1>
    
    <script src="static/js/main.js"></script>
</body>
</html>
""")