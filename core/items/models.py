import uuid
from django.db import models
from core.rubros.models import Rubro


# Create your models here.
class Item(models.Model):
    id = models.UUIDField("id", primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField("description", max_length=150, blank=True, null=True)
    justificacion = models.TextField(
        "justificacion", max_length=150, blank=True, null=True
    )
    quantity = models.IntegerField("quantity", default=0)
    unit_value = models.DecimalField(
        "unit_value", max_digits=10, decimal_places=2, default=0
    )
    total_value = models.DecimalField(
        "total_value", max_digits=10, decimal_places=2, default=0
    )
    rubro = models.ForeignKey(
        Rubro, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)
    deleted_at = models.DateTimeField("deleted_at", blank=True, null=True)

    class Meta:
        db_table = "items"
        ordering = ["id"]
