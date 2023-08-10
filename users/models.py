from django.contrib.auth.hashers import make_password
from django.db import models


class BaseUser(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=150)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.password = make_password(self.password)
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    @property
    def is_authenticated(self):
        return True

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.email}"


class SupportSystemUser(BaseUser):
    pass


class ClientUser(BaseUser):
    pass





