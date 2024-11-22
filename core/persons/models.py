from django.db import models


# Create your models here.
class Person(models.Model):
    job_title = models.CharField("job_title", max_length=100, blank=True, null=True)
    dedication = models.CharField("dedication", max_length=100, blank=True, null=True)
    weeks = models.CharField("weeks", max_length=100, blank=True, null=True)
    fees = models.CharField("fees", max_length=100, blank=True, null=True)
    value_hour = models.DecimalField(
        "value_hour", max_digits=10, decimal_places=2, default=0
    )
    total = models.DecimalField("total", max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)
    deleted_at = models.DateTimeField("deleted_at", blank=True, null=True)

    class Meta:
        db_table = "persons"
        ordering = ["id"]
