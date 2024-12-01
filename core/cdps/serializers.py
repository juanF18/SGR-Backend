from rest_framework import serializers
from .models import Cdps
from core.rubros.serializers import RubroSerializer

class CdpsSerializer(serializers.ModelSerializer):
    rubro = RubroSerializer(many=False)

    class Meta:
        model = Cdps
        exclude = ["created_at", "updated_at", "deleted_at"]

    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("rubro"):
            representation["rubro_id"] = data.rubro.get("id")
        else:
            representation["rubro_id"] = None
        return representation
