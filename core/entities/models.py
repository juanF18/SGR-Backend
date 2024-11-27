import uuid
from django.db import models


# Create your models here.
class Entity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField("name", max_length=100, null=True, blank=True)
    nit = models.CharField("nit", max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField("email", max_length=100, null=True, blank=True)
    phone = models.CharField("phone", max_length=100, null=True, blank=True)
    address = models.CharField("address", max_length=100, null=True, blank=True)
    city = models.CharField("city", max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "entities"
        ordering = ["id"]
