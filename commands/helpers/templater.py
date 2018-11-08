from jinja2 import Template as JTemplate
import inflect


p = inflect.engine()


attribute_template = JTemplate("""{{ name }} = models.{{ type }}({{ options }})""")


model_template = JTemplate("""
class {{ model }}(models.Model):

	{% for attribute in attributes %}{% if loop.index > 1 %}\t{% endif %}{{ attribute }}\n{% endfor %}
	class Meta:
		db_table = '{{ model }}_table'

	def __str__(self):
		return None
""")


model_admin_template = JTemplate("""
class {{ model }}Admin(admin.ModelAdmin):
	pass
	
admin.site.register({{ model }}, {{model}}Admin)
""")


route_template = JTemplate("""
def {{ route }}(request):
	context = {
		active: True,
		route: '{{ route }}',
	 }
	return render(request, '{{ route }}.html', context)
""")


form_template = JTemplate("""
class {{ model }}Form(forms.Form):
	class Meta:
		model = {{ model }}
		fields = "__all__"
""")


serializer_template = JTemplate("""
class {{ model }}Serializer(serializers.ModelSerializer):
	
	# If model has foreign key to another model, add it like so:
	# models = serializers.StringRelatedField(many=True)
	
	class Meta:
		model = {{ model }}
		fields = "__all__"
""")

viewset_template = JTemplate("""
class {{ model }}Viewset(viewsets.ModelViewSet):
	queryset = {{ model }}.objects.all()
	serializer_class = {{ model }}Serializer
""")
