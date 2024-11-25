from django.db import models
from core.entities.models import Entity


# Create your models here.
class Project(models.Model):
    name = models.CharField("name", max_length=100, blank=True, null=True)
    description = models.TextField("description", blank=True, null=True)
    value = models.DecimalField("value", max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField("start_date", blank=True, null=True)
    end_date = models.DateField("end_date", blank=True, null=True)
    file_budget_url = models.CharField(
        "file_budget_url", max_length=150, blank=True, null=True
    )
    file_activities_url = models.CharField(
        "file_activities_url", max_length=150, blank=True, null=True
    )
    entity_id = models.ForeignKey(
        Entity, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)
    deleted_at = models.DateTimeField("deleted_at", blank=True, null=True)

    class Meta:
        db_table = "projects"
        ordering = ["id"]
