from rest_framework import serializers
from .models import Contract
from core.cdps.serializers import CdpsSerializer

class ContractSerializer(serializers.ModelSerializer):
    cdps = CdpsSerializer(many=False)

    class Meta:
        model = Contract
        exclude = ["created_at", "updated_at", "deleted_at"]

    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("cdps"):
            representation["cdps_id"] = data.cdps.get("id")
        else:
            representation["cdps_id"] = None
        return representation
