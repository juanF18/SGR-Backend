from rest_framework import serializers
from .models import Role
<<<<<<< HEAD
from django import forms
from django.core import validators


class RoleValidator(forms.Form):
    """
    RoleValidator is a form that validates the name of a role.
    """

    name = forms.CharField(
        max_length=50,
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r"^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$",
                code="invalid_name",
            )
        ],
    )

=======
>>>>>>> develop

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
<<<<<<< HEAD
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["name"] = instance.name
        return representation
=======
        fields = '__all__'

    def to_representation(self, instance):
      representation = super().to_representation(instance)
      representation['name'] = instance.name
      return representation
>>>>>>> develop
