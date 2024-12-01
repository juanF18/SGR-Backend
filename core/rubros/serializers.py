from rest_framework import serializers
from .models import Rubro
from core.projects.serializers import ProjectSerializer

class RubroSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(many=False)

    class Meta:
        model = Rubro
        exclude =  ["created_at", "updated_at", "deleted_at"]

    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("project"):
            representation["project_id"] = data.project.get("id")
        else:
            representation["project_id"] = None
        return representation
