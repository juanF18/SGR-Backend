from rest_framework import serializers
from .models import MovementCounterpart


class MovementCounterpartSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementCounterpart
        exclude = ["created_at", "updated_at", "deleted_at"]

    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("counterpart_execution"):
            representation["counterpart_execution_id"] = data.get(
                "counterpart_execution"
            ).get("id")
        else:
            representation["counterpart_execution_id"] = None
        return representation
