from django.db import models
from core.tasks.models import Task
from core.contracts.models import Contract


# Create your models here.
class DetailContract(models.Model):
    description = models.CharField("description", max_length=150, null=True, blank=True)
    start_date = models.DateField("start_date", null=True, blank=True)
    end_date = models.DateField("end_date", null=True, blank=True)
    state = models.BooleanField("state", default=False)
    task_id = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    contract_id = models.ForeignKey(
        Contract, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "detail_contracts"
        ordering = ["id"]
