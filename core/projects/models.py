import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from core.entities.models import Entity
from .helpers import RenameFileWithProjectID


# Create your models here.
class Project(models.Model):
    id = models.UUIDField(
        "id", primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField("name", max_length=250, blank=True, null=True)
    description = models.TextField("description", blank=True, null=True)
    value = models.DecimalField("value", max_digits=18, decimal_places=1, default=0)
    start_date = models.DateField("start_date", null=True, default=timezone.now)
    end_date = models.DateField("end_date", null=True, default=timezone.now)
    file_budget = models.FileField(
        "file_budget",
        upload_to=RenameFileWithProjectID("budgets"),
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["xlsx"])],
    )
    file_activities = models.FileField(
        "file_activities",
        upload_to=RenameFileWithProjectID("activities"),
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["xlsx"])],
    )
    entity = models.ForeignKey(Entity, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)
    deleted_at = models.DateTimeField("deleted_at", blank=True, null=True)

    class Meta:
        db_table = "projects"
        ordering = ["id"]
