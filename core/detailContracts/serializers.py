from rest_framework import serializers
from .models import DetailContract
from core.tasks.serializers import TaskSerializer
from core.contracts.serializers import ContractSerializer


class DetailContractSerializer(serializers.ModelSerializer):
    task = TaskSerializer(many=False)
    contract = ContractSerializer(many=False)

    class Meta:
        model = DetailContract
        exclude = ["created_at", "updated_at", "deleted_at"]

    def to_internal_value(self, data):
        representation = super().to_internal_value(data)
        if data.get("task"):
            representation["task_id"] = data.task.get("id")
        else:
            representation["task_id"] = None
        if data.get("contract"):
            representation["contract_id"] = data.contract.get("id")
        else:
            representation["contract_id"] = None
        return representation
