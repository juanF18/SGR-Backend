from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MovementsCounterparts
from .serializers import MovementCounterpartSerializer
from core.counterpartExecution.models import CounterpartExecution
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Definir el cuerpo de la solicitud para el POST y PUT
movement_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "amount": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="Monto del movimiento"
        ),
        "description": openapi.Schema(
            type=openapi.TYPE_STRING, description="Descripción del movimiento"
        ),
        "type": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Tipo de movimiento (I: Ingresos, G: Gastos)",
        ),
        "counterpart_execution_id": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="ID de la ejecución de contraparte asociada",
        ),
    },
)


class MovementCounterpartView(APIView):
    """
    Class to handle HTTP requests related to MovementCounterpart
    """

    @swagger_auto_schema(
        operation_description="Obtener todos los movimientos de contrapartidas",
        responses={
            200: openapi.Response(
                description="Movimientos recuperados correctamente",
                schema=MovementCounterpartSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):
        """
        Get all MovementCounterpart
        """
        try:
            movements = MovementsCounterparts.objects.all()
            serializer = MovementCounterpartSerializer(movements, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": f"Error al obtener los movimientos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Crear un nuevo movimiento de contraparte",
        request_body=movement_request_body,
        responses={
            201: openapi.Response(
                description="Movimiento creado correctamente",
                schema=MovementCounterpartSerializer,
            ),
            400: openapi.Response(description="Error en los datos de entrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):
        """
        Create a new MovementCounterpart
        """
        try:
            data = request.data
            counterpart_execution = CounterpartExecution.objects.get(
                id=data["counterpart_execution_id"]
            )

            movement = MovementsCounterparts.objects.create(
                amount=data["amount"],
                description=data["description"],
                type=data["type"],
                counterpart_execution=counterpart_execution,
            )

            serializer = MovementCounterpartSerializer(movement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except CounterpartExecution.DoesNotExist:
            return Response(
                {"message": "Ejecución de contraparte no encontrada"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": f"Error al crear el movimiento: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MovementCounterpartDetailView(APIView):
    """
    Class to handle specific MovementCounterpart requests
    """

    @swagger_auto_schema(
        operation_description="Obtener los detalles de un movimiento específico",
        responses={
            200: openapi.Response(
                description="Movimiento recuperado correctamente",
                schema=MovementCounterpartSerializer,
            ),
            400: openapi.Response(description="Movimiento no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, movement_id):
        """
        Get specific MovementCounterpart by ID
        """
        try:
            movement = MovementsCounterparts.objects.get(id=movement_id)
            serializer = MovementCounterpartSerializer(movement)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MovementsCounterparts.DoesNotExist:
            return Response(
                {"message": "Movimiento no encontrado"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": f"Error al obtener el movimiento: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Actualizar un movimiento específico por ID",
        request_body=movement_request_body,
        responses={
            200: openapi.Response(
                description="Movimiento actualizado correctamente",
                schema=MovementCounterpartSerializer,
            ),
            400: openapi.Response(description="Movimiento no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def put(self, request, movement_id):
        """
        Update specific MovementCounterpart by ID
        """
        try:
            movement = MovementsCounterparts.objects.get(id=movement_id)
            data = request.data

            if "counterpart_execution_id" in data:
                movement.counterpart_execution = CounterpartExecution.objects.get(
                    id=data["counterpart_execution_id"]
                )

            movement.amount = data.get("amount", movement.amount)
            movement.description = data.get("description", movement.description)
            movement.type = data.get("type", movement.type)

            movement.save()

            serializer = MovementCounterpartSerializer(movement)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except MovementsCounterparts.DoesNotExist:
            return Response(
                {"message": "Movimiento no encontrado"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except CounterpartExecution.DoesNotExist:
            return Response(
                {"message": "Ejecución de contraparte no encontrada"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": f"Error al actualizar el movimiento: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Eliminar un movimiento específico por ID",
        responses={
            200: openapi.Response(description="Movimiento eliminado correctamente"),
            400: openapi.Response(description="Movimiento no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def delete(self, request, movement_id):
        """
        Delete specific MovementCounterpart by ID
        """
        try:
            movement = MovementsCounterparts.objects.get(id=movement_id)
            movement.delete()
            return Response(
                {"message": "Movimiento eliminado correctamente"},
                status=status.HTTP_200_OK,
            )
        except MovementsCounterparts.DoesNotExist:
            return Response(
                {"message": "Movimiento no encontrado"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": f"Error al eliminar el movimiento: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MovementCounterpartSumView(APIView):
    """
    Endpoint para obtener la suma total de los movimientos por tipo
    """

    @swagger_auto_schema(
        operation_description="Obtener la suma total de los movimientos por tipo",
        responses={
            200: openapi.Response(
                description="Sumas calculadas correctamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "total_ingresos": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Suma total de los ingresos",
                        ),
                        "total_gastos": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Suma total de los gastos",
                        ),
                        "total_general": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Suma total general (ingresos - gastos)",
                        ),
                    },
                ),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):
        """
        Calcula la suma total de los movimientos agrupados por tipo
        """
        try:
            total_ingresos = (
                MovementsCounterparts.objects.filter(type="I").aggregate(
                    total=Sum("amount")
                )["total"]
                or 0
            )
            total_gastos = (
                MovementsCounterparts.objects.filter(type="G").aggregate(
                    total=Sum("amount")
                )["total"]
                or 0
            )

            total_general = total_ingresos - total_gastos

            return Response(
                {
                    "total_ingresos": total_ingresos,
                    "total_gastos": total_gastos,
                    "total_general": total_general,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": f"Error al calcular las sumas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
