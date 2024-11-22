from django.db import models
from core.rubros.models import Rubro


# Create your models here.
class Travel(models.Model):
    origin = models.CharField("origin", max_length=100, blank=True, null=True)
    destination = models.CharField("destination", max_length=100, blank=True, null=True)
    transport = models.CharField("transport", max_length=100, blank=True, null=True)
    quantity = models.IntegerField("quantity", blank=True, null=True)
    cant_persons = models.IntegerField("cant_persons", blank=True, null=True)
    cant_days = models.IntegerField("cant_days", blank=True, null=True)
    total = models.DecimalField("total", max_digits=10, decimal_places=2, default=0)
    rubro_id = models.ForeignKey(
        Rubro, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "travels"
        ordering = ["id"]
