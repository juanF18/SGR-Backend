import uuid
from django.db import models
from core.projects.models import Project


# Create your models here.
class Rubro(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    descripcion = models.TextField("descripcion", max_length=150, blank=True, null=True)
    value_sgr = models.DecimalField(
        "value_sgr", max_digits=15, decimal_places=1, default=0
    )
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "rubros"
        ordering = ["id"]
