from django.db import models
from core.rubros.models import Rubro


# Create your models here.
class Counterpart(models.Model):
    name = models.CharField(max_length=100)
    value_species = models.DecimalField(
        "value_species", max_digits=10, decimal_places=2, default=0
    )
    value_chash = models.DecimalField(
        "value_chash", max_digits=10, decimal_places=2, default=0
    )
    rubro_id = models.ForeignKey(
        Rubro, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "counterparts"
        ordering = ["id"]
