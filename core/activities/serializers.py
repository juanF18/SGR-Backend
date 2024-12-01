from rest_framework import serializers
from .models import Activity
from core.rubros.serializers import RubroSerializer
from core.projects.serializers import ProjectSerializer

class ActivitySerializer(serializers.ModelSerializer):
    rubro = RubroSerializer(many=False)
    project = ProjectSerializer(many=False)

    class Meta:
        model = Activity
        exclude = ["created_at", "updated_at", "deleted_at"]    
    
    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("rubro"):
            representation["rubro_id"] = data.rubro.get("id")
        else:
            representation["rubro_id"] = None
        if data.get("project"):
            representation["project_id"] = data.project.get("id")
        else:
            representation["project_id"] = None
        return representation