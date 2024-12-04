from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from core.roles.serializers import RoleSerializer
from core.entities.serializers import EntitySerializer
from django import forms
from django.core import validators


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=False)
    entity = EntitySerializer(many=False)

    class Meta:
        model = User
        exclude = [
            "created_at",
            "updated_at",
            "deleted_at",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
        ]

    def validate_email(self, email):
        """Valida que el email sea único"""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("El email ya existe")
        return email

    def to_internal_value(self, data):
        """Ajusta los valores internos del usuario"""
        representation = super().to_internal_value(data)
        if data.get("role"):
            representation["role_id"] = data["role"].get("id")
        else:
            representation["role_id"] = None
        if data.get("entity"):
            representation["entity_id"] = data.entity.get("id")
        else:
            representation["entity_id"] = None
        return representation

    def create(self, validated_data):
        """Crear un nuevo usuario con la contraseña cifrada"""
        password = validated_data.pop("password", None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(
                password
            )  # Asegurarse de que la contraseña se guarde correctamente
        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    role_name = serializers.CharField(read_only=True)
    entity_name = serializers.CharField(read_only=True)

    def validate(self, attrs):
        """
        Valida las credenciales de login (email y contraseña).
        """
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
            print(f"User found: {user.id}")
        except User.DoesNotExist:
            raise serializers.ValidationError("El usuario no existe")

        # Verifica que la contraseña sea correcta
        if not user.check_password(password):
            raise serializers.ValidationError("Credenciales incorrectas (password)")

        # Genera tokens de acceso
        print(f"Generating tokens for user ID: {user.id}")
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        print(f"Generated Access Token: {access_token}")

        user_data = {
            "first_name": user.name,
            "last_name": user.last_name,
            "email": user.email,
            "role_name": user.role.name if user.role else None,
            "entity_name": user.entity.name if user.entity else None,
            "refresh": str(refresh),
            "access": str(access_token),
        }

        return user_data


class UserValidator(forms.Form):
    """
    Formulario de validación de los datos básicos del usuario.
    """

    name = forms.CharField(
        max_length=100,
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r"^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$",
                code="invalid_name",
            )
        ],
    )

    last_name = forms.CharField(
        max_length=100,
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r"^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$",
                code="invalid_last_name",
            )
        ],
    )

    email = forms.EmailField(
        max_length=100,
        required=True,
        validators=[
            validators.EmailValidator(
                code="invalid_email",
            )
        ],
    )

    identification = forms.CharField(
        max_length=100,
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r"^[0-9]+$",
                code="invalid_identification",
            )
        ],
    )
