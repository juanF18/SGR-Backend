from rest_framework import serializers
from .models import DetailContract


class DetailContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailContract
        fields = "__all__"
