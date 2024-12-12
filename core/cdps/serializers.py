from rest_framework import serializers
from .models import Cdps
from core.rubros.serializers import RubroSerializer
from core.activities.serializers import ActivitySerializer


class CdpsSerializer(serializers.ModelSerializer):
    rubro = RubroSerializer(many=False)
    activity = ActivitySerializer(many=False)

    class Meta:
        model = Cdps
        exclude = ["created_at", "updated_at", "deleted_at"]

    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("rubro"):
            representation["rubro_id"] = data.rubro.get("id")
        else:
            representation["rubro_id"] = None
        if data.get("activity"):
            representation["activity_id"] = data.activity.get("id")
        else:
            representation["activity_id"] = None
        return representation
