import uuid
from django.db import models


# Create your models here.
class Activity(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField("name", max_length=150, null=True, blank=True)
    description = models.TextField("description", null=True, blank=True)
    type = models.CharField("type", max_length=150, null=True, blank=True)
    start_date = models.DateField("start_date", null=True, blank=True)
    end_date = models.DateField("end_date", null=True, blank=True)
    state = models.CharField("state", max_length=150, null=True, blank=True)
    project_id = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, null=True, blank=True
    )
    rubro_id = models.ForeignKey(
        "rubros.Rubro", on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)
    deleted_at = models.DateTimeField("deleted_at", null=True, blank=True)

    class Meta:
        db_table = "activities"
        ordering = ["id"]
