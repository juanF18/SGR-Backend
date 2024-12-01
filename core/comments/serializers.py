from rest_framework import serializers
from .models import Comment
from core.users.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Comment
        exclude = ["created_at", "updated_at", "deleted_at"]


    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("user"):
            representation["user_id"] = data.user.get("id")
        else:
            representation["user_id"] = None
        return representation