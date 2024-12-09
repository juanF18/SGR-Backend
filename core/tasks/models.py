import uuid
from django.db import models
from core.activities.models import Activity


# Create your models here.
class Task(models.Model):
    id = models.UUIDField(
        "id", primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    task_num = models.IntegerField("task_num", default=0)
    name = models.CharField("name", max_length=500, null=True, blank=True)
    description = models.TextField("description", null=True, blank=True)
    start_date = models.DateField("start_date", null=True, blank=True)
    end_date = models.DateField("end_date", null=True, blank=True)
    state = models.CharField("state", max_length=100, null=True, blank=True)
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)
    deleted_at = models.DateTimeField("deleted_at", null=True, blank=True)

    class Meta:
        db_table = "tasks"
        ordering = ["task_num"]
