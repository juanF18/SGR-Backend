from rest_framework import serializers
from .models import Movement
from core.contracts.serializers import ContractSerializer

class MovementSerializer(serializers.ModelSerializer):
    contract = ContractSerializer(many=False)

    class Meta:
        model = Movement
        exclude = ["created_at", "updated_at", "deleted_at"]

    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("contract"):
            representation["contract_id"] = data.contract.get("id")
        else:
            representation["contract_id"] = None
        return representation
