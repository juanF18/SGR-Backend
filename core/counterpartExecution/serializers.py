from rest_framework import serializers
from .models import CounterpartExecution
from core.counterparts.serializers import CounterpartSerializer
from core.activities.serializers import ActivitySerializer


class CounterpartExecutionSerializer(serializers.ModelSerializer):
    counterpart = CounterpartSerializer(many=False)
    activity = ActivitySerializer(many=True)

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
        if data.get("activity"):
            representation["activity_id"] = data.activity.get("id")
        else:
            representation["activity_id"] = None
