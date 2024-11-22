from rest_framework import serializers
from .models import cdps


class CDPSSerializer(serializers.ModelSerializer):
    class Meta:
        model = cdps
        fields = "__all__"
