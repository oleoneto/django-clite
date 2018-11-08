from string import Template



"""
On Templated strings:
	Create route or view:
		- lowercase the $routeName
		- Create an html page with the same name under the directory
		- i.e Homepage -> homepage
	Create model, form, serializer, admin:
		- First letter of model should be uppercase
		- Enforce singular nouns (prompt if 's' is detected at end of a name)
		- i.e users -> User	
"""	


def sanitized(str):
	
	new = str
	new = new.replace("{{", "")
	new = new.replace("}}", "")
	
	return new


view = """
def $routeName(request):
	context = {
		active: True,
		route: '$routeName',
	 }
	return render(request, '$routeName.html', context)
"""
v = Template(view)
v = v.substitute(routeName="home")
#print(v)


# ------------
# ------------
# ------------

form = """
class $modelName{{Admin}}(forms.Form):
	class Meta:
		model = $modelName
		fields = "__all__"
"""

f = Template(form)
f = f.substitute(modelName='Artist')
#print(sanitized(f))


# -----------------
# -----------------
# -----------------

viewset = """
class $modelName{{Viewset}}(viewsets.ModelViewSet):
	queryset = $modelName.objects.all()
	serializer_class = $modelName{{Serializer}}
"""

v = Template(viewset)
v = v.substitute(modelName="Music")
#print(sanitized(v))


# --------------------
# --------------------
# --------------------

model = """
class $modelName(models.Model):
	$attributeName = models.$attributeType($attributeOptions)

	class Meta:
		abstract = False
		db_table = '$modelName.table'

	def __str__(self):
		return None
"""
m = Template(model)
m = m.substitute(modelName="User", attributeName="first_name", attributeType="CharField", attributeOptions="max_length=5")
#print(sanitized(m))
#print(sanitized.__name__)


# -----------------------
# $attributeName = models.$attributeType($attributeOptions)

from jinja2 import Template

attribute = "{{attributeName}} = models.{{attributeType}}({{attributeOptions}})"
model = """
class {{modelName}}(models.Model):
	{{ attributes }}
	class Meta:
		abstract = False
		db_table = '{{modelName}}_table'

	def __str__(self):
		return None
"""
t = Template(model)
t = t.render(modelName='User', attributes="photo = model.ImageField()")
print(t)




import inflect

p = inflect.engine()

word = "Ox"
print("The plural of", word, "is", p.plural(word))




from enum import Enum

class ModelType(Enum):
	FK ="ForeignKey"
	One = "OneToOneField"
	
print(ModelType.One.value)