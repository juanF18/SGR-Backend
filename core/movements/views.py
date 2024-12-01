from rest_framework import status
from rest_framework.response import Response
from .models import Movement
from rest_framework.views import APIView
from .serializers import MovementSerializer
from core.contracts.models import Contract
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Definir el cuerpo de la solicitud para el POST en MovementView
movement_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "amount": openapi.Schema(
            type=openapi.TYPE_NUMBER,
            format=openapi.FORMAT_FLOAT,
            description="Monto del movimiento",
        ),
        "description": openapi.Schema(
            type=openapi.TYPE_STRING, description="Descripción del movimiento"
        ),
        "type": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Tipo de movimiento (ingreso, egreso, etc.)",
        ),
        "contract_id": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="ID del contrato relacionado con el movimiento",
        ),
    },
)


class MovementView(APIView):

    """
    Class to handle HTTP requests related to movements

    @methods:
    - get: Get all movements
    - post: Create a new movement
    """

    # Documentar el método GET para obtener todos los movimientos
    @swagger_auto_schema(
        operation_description="Obtener todos los movimientos",
        responses={
            200: openapi.Response(
                description="Movimientos recuperados correctamente",
                schema=MovementSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):

        """
        Get all movements
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = Movement.objects.all()
            movement_serializer = MovementSerializer(data, many=True)

            return Response(movement_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving movements: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método POST para crear un movimiento
    @swagger_auto_schema(
        operation_description="Crear un nuevo movimiento",
        request_body=movement_request_body,
        responses={
            201: openapi.Response(
                description="Movimiento creado correctamente", schema=MovementSerializer
            ),
            400: openapi.Response(description="Contrato no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):

        """
        Create a new movement
        @param request: HTTP request
        @return: JSON response
        """

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

            return Response(movement_serializer.data, status=status.HTTP_201_CREATED)
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

    """
    Class to handle HTTP requests related to a specific movement

    @methods:
    - get: Get a specific movement by ID
    """

    # Documentar el método GET para obtener un movimiento específico por ID
    @swagger_auto_schema(
        operation_description="Obtener un movimiento específico por ID",
        responses={
            200: openapi.Response(
                description="Movimiento recuperado correctamente",
                schema=MovementSerializer,
            ),
            400: openapi.Response(description="Movimiento no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, id):
        try:
            movement = Movement.objects.get(id=id)
            movement_serializer = MovementSerializer(movement, many=False)

            return Response(movement_serializer.data, status=status.HTTP_200_OK)
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
