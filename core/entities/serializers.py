from rest_framework import serializers
from .models import Entity
from django import forms
from django.core import validators


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"


class EntityValidator(forms.Form):
    """
    EntityValidator class is used to validate the data of the entity
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

    nit = forms.CharField(
        max_length=100,
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r"^\d{9,10}-\d{1}$",
                code="invalid_nit",
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

    phone = forms.CharField(
        max_length=100,
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r"^\d{10}$",
                code="invalid_phone",
            )
        ],
    )

    address = forms.CharField(
        max_length=100,
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r"^[A-Za-z0-9\s\#\-,.áéíóúÁÉÍÓÚñÑ]+$",
                code="invalid_address",
            )
        ],
    )

    city = forms.CharField(
        max_length=100,
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r"^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$",
                code="invalid_city",
            )
        ],
    )
