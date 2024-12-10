from rest_framework import serializers
from .models import Movement
from core.cdps.serializers import CdpsSerializer
class MovementSerializer(serializers.ModelSerializer):
    cdp = CdpsSerializer(many=False)

    class Meta:
        model = Movement
        exclude = ["created_at", "updated_at", "deleted_at"]

    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("cdp"):
            representation["cdp_id"] = data.get("cdp").get("id")
        else:
            representation["cdp_id"] = None
        return representation
