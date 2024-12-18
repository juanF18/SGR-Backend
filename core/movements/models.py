import uuid
from django.db import models
from core.cdps.models import Cdps

choices = (("I", "Income"), ("E", "Expense"))


# Create your models here.
class Movement(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    amount = models.DecimalField("amount", max_digits=20, decimal_places=2, default=0)
    description = models.CharField("description", max_length=500, blank=True, null=True)
    type = models.CharField("type", max_length=1, choices=choices, default="I")
    cdp = models.ForeignKey(Cdps, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "movements"
        ordering = ["id"]
