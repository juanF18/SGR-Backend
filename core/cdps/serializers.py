from rest_framework import serializers
from .models import Cdps


class CdpsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cdps
        fields = "__all__"
