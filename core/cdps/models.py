import uuid
from django.db import models
from core.rubros.models import Rubro
from core.activities.models import Activity


# Create your models here.
class Cdps(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    number = models.CharField("number", max_length=50, null=True, blank=True)
    expedition_date = models.DateField("expedition_date", null=True, blank=True)
    amount = models.DecimalField(
        "amount", max_digits=20, decimal_places=2, null=True, blank=True
    )
    description = models.TextField("description", null=True, blank=True)
    is_generated = models.BooleanField("is_generated", default=False)
    is_canceled = models.BooleanField("is_canceled", default=False)
    rubro = models.ForeignKey(Rubro, on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.ForeignKey(
        Activity, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "cdps"
        ordering = ["id"]
