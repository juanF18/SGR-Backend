import uuid
from django.db import models
from core.contracts.models import Contract

choices = (("I", "Income"), ("E", "Expense"))


# Create your models here.
class Movement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    amount = models.DecimalField("amount", max_digits=10, decimal_places=2, default=0)
    description = models.CharField("description", max_length=150, blank=True, null=True)
    type = models.CharField("type", max_length=1, choices=choices, default="I")
    contract = models.ForeignKey(
        Contract, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "movements"
        ordering = ["id"]
