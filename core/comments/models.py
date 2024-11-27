from django.db import models
from core.users.models import User


# Create your models here.
class Comment(models.Model):
    comment_text = models.TextField("comment_text", null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)
    deleted_at = models.DateTimeField("deleted_at", null=True, blank=True)

    class Meta:
        db_table = "comments"
        ordering = ["id"]