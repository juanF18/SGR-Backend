from rest_framework import serializers
from .models import Rubro


class RubroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubro
        fields = "__all__"
