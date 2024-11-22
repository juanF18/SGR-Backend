from django.db import models


# Create your models here.
class Role(models.Model):
    name = models.CharField("name", max_length=50, unique=True, null=False, blank=False)
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)
    deleted_at = models.DateTimeField("deleted_at", null=True, blank=True)

    class Meta:
        db_table = "roles"
        ordering = ["id"]
