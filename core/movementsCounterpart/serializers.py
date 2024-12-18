from rest_framework import serializers
from .models import MovementsCounterparts
from core.counterpartExecution.serializers import CounterpartExecutionSerializer


class MovementCounterpartSerializer(serializers.ModelSerializer):
    counterpart_execution = CounterpartExecutionSerializer(many=False)  # Corregido

    class Meta:
        model = MovementsCounterparts
        exclude = ["created_at", "updated_at", "deleted_at"]

    def to_internal_value(self, data):
        representation = super().to_internal_value(data)

        # Manejo de la relación con CounterpartExecution
        counterpart_execution_data = data.get("counterpart_execution")
        if counterpart_execution_data:
            representation["counterpart_execution_id"] = counterpart_execution_data
        else:
            representation["counterpart_execution_id"] = None

        return representation
