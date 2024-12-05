from rest_framework import serializers
from .models import Project
from django import forms
from django.core import validators
from core.entities.serializers import EntitySerializer


class ProjectSerializer(serializers.ModelSerializer):
    entity = EntitySerializer(many=False)
    file_budget_url = serializers.SerializerMethodField()
    file_activities_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        exclude = [
            "created_at",
            "updated_at",
            "deleted_at",
            "file_budget",
            "file_activities",
        ]

    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("entity"):
            representation["entity_id"] = data.entity.get("id")
        else:
            representation["entity_id"] = None
        return representation

    def get_file_budget_url(self, obj):
        """
        Generate full URL for the file_budget field
        """
        request = self.context.get("request")
        if obj.file_budget:
            file_url = obj.file_budget.url
            return self.build_absolute_url(request, file_url)
        return None

    def get_file_activities_url(self, obj):
        """
        Generate full URL for the file_activities field
        """
        request = self.context.get("request")
        if obj.file_activities:
            file_url = obj.file_activities.url
            return self.build_absolute_url(request, file_url)
        return None

    def build_absolute_url(self, request, file_url):
        """
        Helper method to generate the full URL based on the request.
        """
        if not request:
            return file_url
        return f"{request.scheme}://{request.get_host()}{file_url}"


class ProjectFileSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(required=True)
    value = serializers.DecimalField(
        max_digits=20,  # 12 dígitos en total
        decimal_places=2,  # 2 decimales (por ejemplo, para representar centavos)
        required=True,
    )
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    file_budget = serializers.FileField(
        required=False,
        validators=[validators.FileExtensionValidator(allowed_extensions=["xlsx"])],
    )
    file_activities = serializers.FileField(
        required=False,
        validators=[validators.FileExtensionValidator(allowed_extensions=["xlsx"])],
    )
    entity_id = serializers.UUIDField(required=True)


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
        max_length=300,
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r"[\w\Wa-zA-ZáéíóúÁÉÍÓÚ\s]+$",
                code="invalid_description",
            )
        ],
    )

    value = forms.DecimalField(
        max_digits=15,
        decimal_places=1,
        required=True,
        validators=[
            validators.MinValueValidator(0),
        ],
    )

    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)
