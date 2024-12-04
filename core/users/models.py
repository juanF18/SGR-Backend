from django.db import models
from core.roles.models import Role
from core.entities.models import Entity
import uuid
import os
import hashlib


class User(models.Model):
    # Campos principales
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField("Correo electrónico", unique=True)
    name = models.CharField("Nombre", max_length=100, null=True, blank=True)
    last_name = models.CharField("Apellido", max_length=100, null=True, blank=True)
    identification = models.CharField("Identificación", max_length=50, unique=True)
    password = models.CharField("Contraseña", max_length=256)

    # Campos de estado
    is_active = models.BooleanField(default=True)  # Activo o no
    is_staff = models.BooleanField(default=False)  # Si es administrador
    is_superuser = models.BooleanField(default=False)  # Si es superusuario

    # Relaciones
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    entity = models.ForeignKey(Entity, on_delete=models.SET_NULL, null=True, blank=True)

    # Tiempos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["identification", "password"]

    class Meta:
        db_table = "users"
        ordering = ["id"]

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        """Este método crea el hash de la contraseña"""
        salt = os.urandom(32)  # 32 bytes salt
        hashed_pw = hashlib.pbkdf2_hmac(
            "sha256", raw_password.encode("utf-8"), salt, 100000
        )
        self.password = f"pbkdf2_sha256${salt.hex()}${hashed_pw.hex()}"
        self.save()

    def check_password(self, raw_password):
        """Este método compara el hash con la contraseña ingresada"""
        try:
            algorithm, salt, hashed_pw = self.password.split("$")
            salt = bytes.fromhex(salt)
            stored_hashed_pw = bytes.fromhex(hashed_pw)
            hashed_input_pw = hashlib.pbkdf2_hmac(
                "sha256", raw_password.encode("utf-8"), salt, 100000
            )
            return hashed_input_pw == stored_hashed_pw
        except Exception as e:
            print("Error al verificar la contraseña", e)
            return False

    # Métodos que Django espera para autenticación
    @property
    def is_authenticated(self):
        return True if self.is_active else False

    @property
    def is_anonymous(self):
        return False

    def get_username(self):
        return self.email
