from rest_framework import serializers
from .models import Task
from core.activities.serializers import ActivitySerializer


class TaskSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(many=False)

    class Meta:
        model = Task
        exclude = ["created_at", "updated_at", "deleted_at"]

    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("activity"):
            representation["activity_id"] = data.activity.get("id")
        else:
            representation["activity_id"] = None
        return representation
