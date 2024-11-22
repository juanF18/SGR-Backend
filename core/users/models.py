from django.db import models
from core.roles.models import Role
from core.entities.models import Entity


# Create your models here.
class User(models.Model):
    name = models.CharField("name", max_length=100, null=True, blank=True)
    last_name = models.CharField("last_name", max_length=100, null=True, blank=True)
    identification = models.CharField(
        "identification", max_length=100, null=True, blank=True
    )
    password = models.CharField("password", max_length=100, null=True, blank=True)
    role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    entity_id = models.ForeignKey(
        Entity, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "users"
        ordering = ["id"]
