from rest_framework import serializers
from .models import Counterpart


class CounterpartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counterpart
        fields = "__all__"
        depth = 1
