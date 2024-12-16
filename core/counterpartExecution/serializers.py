from rest_framework import serializers
from .models import CounterpartExecution
from core.counterparts.serializers import CounterpartSerializer
from core.cdps.serializers import CdpsSerializer


class CounterpartExecutionSerializer(serializers.ModelSerializer):
    counterpart = CounterpartSerializer(many=False)
    cdp = CdpsSerializer(many=False)

    class Meta:
        model = CounterpartExecution
        exclude = ["created_at", "updated_at", "deleted_at"]
        depth = 1

    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("counterpart"):
            representation["counterpart_id"] = data.counterpart.get("id")
        else:
            representation["counterpart_id"] = None
        if data.get("cdp"):
            representation["cdp_id"] = data.cdp.get("id")
        else:
            representation["cdp_id"] = None
        return representation
