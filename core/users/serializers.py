from rest_framework import serializers
from .models import User
<<<<<<< HEAD
from core.roles.serializers import RoleSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django import forms
from django.core import validators


class UserSerializer(serializers.ModelSerializer):

    role = RoleSerializer(many=False)

    class Meta:
        model = User
        fields = "__all__"

    def validate_identification(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return email

    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("role"):
            representation["role_id"] = data.role.get("id")
        else:
            representation["role_id"] = None
        representation.pop("password")
        return representation


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role_id.name
        return token


class UserValidator(forms.Form):
    """
    UserValidator is a form that validates the name, last name, and identification of a user.
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
=======


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
>>>>>>> develop
