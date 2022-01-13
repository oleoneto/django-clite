import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _


def file_upload_path(instance, filename):
    name, extension = filename.split('.')
    filename = f'{instance.uuid}.{extension}'
    return f'people/{filename}'


class User(AbstractUser):
    photo = models.ImageField(_('photo'), upload_to=file_upload_path, blank=True)
    has_verification = models.BooleanField(
        default=False,
        help_text='Used to distinguish between top accounts of interest',
        verbose_name=_('has verification'),
    )

    # Default fields. Used for record-keeping.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, editable=False)

    class Meta:
        db_table = '{{ db_table.lower() }}'
        ordering = ['-created_at']

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def token(self):
        return Token.objects.get_or_create(user_id=self.id)

    def clean(self):
        """
        Ensure username is always lowercase.
        """
        super().clean()
        self.username = self.username.lower()

    def save(self, *args, **kwargs):
        __new_user__ = False
        if not self.id:
            __new_user__ = True
        super().save(*args, **kwargs)
        Token.objects.get_or_create(user_id=self.id)

        """
        Notifying user that account was successfully created
        if __new_user__:
            self.email_user(
                subject='Message from {{ project_name }}',
                message='Your account was successfully created.'
            )
        """

    def __str__(self):
        return self.username
