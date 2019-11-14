from jinja2 import Template

model_field_template = Template("""{{ name }} = {% if not special %}models.{% endif %}{{ type }}({{ options }}, verbose_name=_('{{ lazy_name }}'))""")


model_admin_template = Template(
    """admin.register({{ classname }}
class {{ classname }}Admin(admin.ModelAdmin):
    pass
""")


model_form_template = Template(
    """from django.forms import forms
from {{ app }}.models.{{ model.lower() }} import {{ classname }}


class {{ classname }}Form(forms.Form):
    class Meta:
        model = {{ classname }}
        fields = "__all__"
""")


model_template = Template(
    """import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
{% for model in imports %}{% if model %}from .{{ model.lower() }} import {{ classname }}{% endif %}
{% endfor %}
{% if base %}from {{ base[0] }} import {{ base[1] }}\n\n{% endif %}
class {{ classname }}({% if base %}{{ base[1] }}{% else %}models.Model{% endif %}):
    {% for field in fields %}{{ field }}
    {% endfor %}
    # Default fields. Used for record-keeping.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('uploaded at'), auto_now=True, editable=False)

    class Meta:
        db_table = '{{ db_table.lower() }}'
        ordering = ['-created_at']
        {% if abstract %}abstract = True\n{% endif %}
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.uuid}'
""")

sql_view_template = Template(
    """import uuid
from django.db import models
{% for model in imports %}{% if model %}from .{{ model.lower() }} import {{ classname }}{% endif %}
{% endfor %}
{% if base %}from {{ base[0] }} import {{ base[1] }}\n\n{% endif %}
class {{ classname }}({% if base %}{{ base[1] }}{% else %}models.Model{% endif %}):
    {% for field in fields %}{{ field }}
    {% endfor %}
    class Meta:
        db_table = '{{ db_table.lower() }}'
        managed = False
""")

sql_view_management_template = ("""
migrations.RunSQL(
    \"""
    DROP VIEW IF EXISTS {{ db_table.lower() }};
    CREATE OR REPLACE VIEW {{ db_table.lower() }} AS
        SELECT 
            {% for field in fields %}
                {{ field }}
            {% endfor %} 
        FROM {{ source }};
    \"""
)
""")

auth_user_model_template = Template(
    """import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _


def file_upload_path(instance, filename):
    name, extension = filename.split('.')
    filename = f'{instance.uuid}.{extension}'
    return f'files/people/{filename}'


class User(AbstractUser):
    photo = models.ImageField(_('photo'), upload_to=file_upload_path, blank=True)
    verified = models.BooleanField(_('verified'), default=False, help_text='Used')

    # Default fields. Used for record-keeping.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, editable=False)

    class Meta:
        db_table = 'authentication_users'
        ordering = ['-created_at']

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def token(self):
        return Token.objects.get_or_create(user_id=self.id)

    def clean(self):
        \"""
        Ensure username is always lowercase.
        \"""
        super().clean()
        self.username = self.username.lower()

    def save(self, *args, **kwargs):
        new_user = False
        if not self.id:
            new_user = True
        super().save(*args, **kwargs)
        Token.objects.get_or_create(user_id=self.id)
        
        \"""
        Notifying user that account was successfully created
        if new_user:
            self.email_user(subject='Message from {{ project_name }}',
                            message='Your account was successfully created.')
        \"""

    def __str__(self):
        return self.username
""")

model_import_template = Template("""from .{{ model.lower() }} import {{ classname }}""")
