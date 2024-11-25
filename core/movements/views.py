from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Movement
from rest_framework.views import APIView
from .serializers import MovementSerializer
from core.contracts.models import Contract


# Create your views here.
class MovementView(APIView):
    def get(self, request):
        try:
            data = Movement.objects.all()
            movement_serializer = MovementSerializer(data, many=True)
            response = {
                "message": "Movements retrieved successfully",
                "status": status.HTTP_200_OK,
                "movements": movement_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving movements: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            contract = Contract.objects.get(id=data["contract_id"])
            movement = Movement.objects.create(
                amount=data["amount"],
                description=data["description"],
                type=data["type"],
                contract_id=contract,
            )
            movement_serializer = MovementSerializer(movement, many=False)
            response = {
                "message": "Movement created successfully",
                "status": status.HTTP_201_CREATED,
                "movement": movement_serializer.data,
            }

            return Response(response, status=status.HTTP_201_CREATED)
        except Contract.DoesNotExist:
            response = {
                "message": "Contract does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error creating movement: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovementDetailView(APIView):
    def get(self, request, id):
        try:
            movement = Movement.objects.get(id=id)
            movement_serializer = MovementSerializer(movement, many=False)
            response = {
                "message": "Movement retrieved successfully",
                "status": status.HTTP_200_OK,
                "movement": movement_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Movement.DoesNotExist:
            response = {
                "message": "Movement does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error retrieving movement: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
