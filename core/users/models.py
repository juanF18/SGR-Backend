from django.db import models
from core.roles.models import Role
from core.entities.models import Entity
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# Create your models here.
class CustomManager(models.Manager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.model.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField("name", max_length=100, null=True, blank=True)
    last_name = models.CharField("last_name", max_length=100, null=True, blank=True)
    email = models.EmailField(
        "email", max_length=100, unique=True, null=True, blank=True
    )
    identification = models.CharField(
        "identification", max_length=100, null=True, blank=True
    )
    password = models.CharField("password", max_length=100, null=True, blank=True)
    role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    entity_id = models.ForeignKey(
        Entity, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = CustomManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        ordering = ["id"]
