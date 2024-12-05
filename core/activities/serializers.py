from rest_framework import serializers
from .models import Activity
from core.rubros.serializers import RubroSerializer
from core.projects.models import Project


class ActivitySerializer(serializers.ModelSerializer):
    rubro = RubroSerializer(many=False)
    project_id = serializers.PrimaryKeyRelatedField(
        source="project", queryset=Project.objects.all(), write_only=True
    )

    class Meta:
        model = Activity
        exclude = ["created_at", "updated_at", "deleted_at", "project"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Cambiar el campo 'project' a 'project_id' para que solo muestre el ID
        representation["project_id"] = instance.project.id if instance.project else None

        return representation

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
