from rest_framework import serializers
from .models import Project
from django import forms
from django.core import validators
from core.entities.serializers import EntitySerializer

class ProjectSerializer(serializers.ModelSerializer):
    entity = EntitySerializer(many=False)

    class Meta:
        model = Project
        exclude = ["created_at", "updated_at", "deleted_at"]    

    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("entity"):
            representation["entity_id"] = data.entity.get("id")
        else:
            representation["entity_id"] = None
        return representation


class ProjectValidator(forms.Form):
    """
    Form to validate the project data before saving it to the database.
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

    description = forms.CharField(
        max_length=150,
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r"[\w\Wa-zA-ZáéíóúÁÉÍÓÚ\s]+$",
                code="invalid_description",
            )
        ],
    )

    value = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        validators=[
            validators.MinValueValidator(0),
            validators.MaxValueValidator(9999999999.99),
        ],
    )

    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)
