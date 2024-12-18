from django.db import models
from core.counterpartExecution.models import CounterpartExecution

choices = (("I", "Ingresos"), ("G", "Gastos"))


# Create your models here.
class MovementsCounterparts(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(max_length=1, choices=choices, default="I")
    counterpart_execution = models.ForeignKey(
        CounterpartExecution, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "movements_counterparts"
        ordering = ["id"]
