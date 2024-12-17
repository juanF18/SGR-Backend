from django.shortcuts import render
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import MovementsCounterpart
from .serializers import MovementCounterpartSerializer
from core.counterpartExecution.models import CounterpartExecution
from core.activities.models import Activity
from django.db.models import Sum

# Create your views here.
movement_counterpart_request_body = openapi.Schema(
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
        "counterpart_execution_id": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="ID de la ejecución de la contrapartida asociada al movimiento",
        ),
    },
)


class MovementCounterpartView(APIView):
    """
    Class to handle HTTP requests related to movementsCounterpart

    @methods:
    - get: Get all movementsCounterpart
    - post: Create a new movementCounterpart
    """

    @swagger_auto_schema(
        operation_description="Obtener todos los movimientos",
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
        Get all movements
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = MovementsCounterpart.objects.all()
            movement_counterpart_serializer = MovementCounterpartSerializer(
                data, many=True
            )

            return Response(
                movement_counterpart_serializer.data, status=status.HTTP_200_OK
            )
        except Exception as e:
            response = {
                "message": f"Error obteniendo los movimientos de las ejecuciones: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Crear un nuevo movimiento de contrapartida",
        request_body=movement_counterpart_request_body,
        responses={
            201: openapi.Response(
                description="Movimiento creado correctamente",
                schema=MovementCounterpartSerializer,
            ),
            400: openapi.Response(description="Contrapartida no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):
        """
        Create a new movement of counterpart execution
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = request.data
            counterpart_execution = CounterpartExecution.objects.get(
                id=data["counterpart_execution_id"]
            )
            movement_counterpart = MovementsCounterpart.objects.create(
                amount=data["amount"],
                description=data["description"],
                type=data["type"],
                counterpart_execution_id=counterpart_execution,
            )
            movement_counterpart_serializer = MovementCounterpartSerializer(
                movement_counterpart, many=False
            )

            return Response(
                movement_counterpart_serializer.data, status=status.HTTP_201_CREATED
            )
        except CounterpartExecution.DoesNotExist:
            response = {
                "message": "Ejecución de contrapartida no encontrada",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error creando el movimiento: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovementsCounterpartDetailView(APIView):
    """
    Class to handle HTTP requests related to a specific movement of counterpart execution

    @methods:
    - get: Get a specific movement by ID
    - put: Update a specific movement by ID
    - delete: Delete a specific movement
    """

    @swagger_auto_schema(
        operation_description="Obtener un movimiento de la contrapartida específico por ID",
        responses={
            200: openapi.Response(
                description="Movimiento recuperado correctamente",
                schema=MovementCounterpartSerializer,
            ),
            400: openapi.Response(description="Movimiento no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, id):
        try:
            movement_counterpart = MovementsCounterpart.objects.get(id=id)
            movement_serializer = MovementCounterpartSerializer(
                movement_counterpart, many=False
            )

            return Response(movement_serializer.data, status=status.HTTP_200_OK)
        except MovementsCounterpart.DoesNotExist:
            response = {
                "message": "Movimiento no encontrado",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error obteniendo el movimiento: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Actualizar un movimiento de la contrapartida específico por ID",
        request_body=movement_counterpart_request_body,
        responses={
            200: openapi.Response(
                description="Movimiento actualizado correctamente",
                schema=MovementCounterpartSerializer,
            ),
            400: openapi.Response(description="Movimiento no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def put(self, request, pk):
        try:
            movement = MovementsCounterpart.objects.get(id=pk)

            data = request.data

            if data.get("counterpart_execution_id"):
                counterpart_execution = CounterpartExecution.objects.get(
                    id=data["counterpart_execution_id"]
                )
                movement.counterpart_execution_id = counterpart_execution

            movement.amount = data.get("amount", movement.amount)
            movement.description = data.get("description", movement.description)
            movement.type = data.get("type", movement.type)

            movement.save()

            movement_serializer = MovementCounterpartSerializer(movement, many=False)

            return Response(movement_serializer.data, status=status.HTTP_200_OK)
        except MovementsCounterpart.DoesNotExist:
            response = {
                "message": "Movimiento no encontrado",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except CounterpartExecution.DoesNotExist:
            response = {
                "message": "Ejecución de contrapartida no encontrada",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error actualizando el movimiento: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Eliminar un movimiento específico específico por ID",
        responses={
            200: openapi.Response(description="Movimiento eliminado correctamente"),
            400: openapi.Response(description="Movimiento no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def delete(self, request, pk):
        try:
            movement = MovementsCounterpart.objects.get(id=pk)
            movement.delete()

            return Response(status=status.HTTP_200_OK)
        except MovementsCounterpart.DoesNotExist:
            response = {
                "message": "Movimiento no encontrado",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error eliminando el movimiento: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovementsCounterpartByProjectId(APIView):
    """
    Class to handle HTTP requests related to movements

    @methods:
    - get: Get all movements
    - post: Create a new movement
    - get_movements_by_project: Get movements filtered by project ID
    """

    # Endpoint para obtener movimientos por proyecto
    @swagger_auto_schema(
        operation_description="Obtener movimientos filtrados por ID de proyecto",
        responses={
            200: openapi.Response(
                description="Movimientos recuperados correctamente",
                schema=MovementCounterpartSerializer(many=True),
            ),
            400: openapi.Response(description="Proyecto no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, project_id):
        """
        Obtener movimientos filtrados por el ID del proyecto.
        @param request: HTTP request
        @param project_id: ID del proyecto
        @return: JSON response con los movimientos del proyecto
        """
        try:

            activities = Activity.objects.filter(project_id=project_id)

            counterpart_execution = CounterpartExecution.objects.filter(
                activity__in=activities
            ).values_list("id", flat=True)

            movements = MovementsCounterpart.objects.filter(
                counterpart_execution_id__in=counterpart_execution
            )

            movement_serializer = MovementCounterpartSerializer(movements, many=True)

            return Response(movement_serializer.data, status=status.HTTP_200_OK)

        except Activity.DoesNotExist:
            response = {
                "message": "Proyecto no encontrado",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error obteniendo los movimientos: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovementsCounterpartSumByProjectId(APIView):
    """
    Clase para manejar solicitudes HTTP relacionadas con la suma de movimientos por ID de proyecto
    """

    @swagger_auto_schema(
        operation_description="Obtener la suma total de los movimientos filtrados por ID de proyecto",
        responses={
            200: openapi.Response(
                description="Suma de movimientos obtenida correctamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "total_amount": openapi.Schema(
                            type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT
                        )
                    },
                ),
            ),
            400: openapi.Response(description="Proyecto no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, project_id):
        """
        Obtener la suma total de los movimientos para un proyecto dado, filtrando por el ID del proyecto.
        @param request: HTTP request
        @param project_id: ID del proyecto
        @return: JSON response con la suma total de los movimientos
        """
        try:

            activities = Activity.objects.filter(project_id=project_id)

            if not activities.exists():
                return Response(
                    {"message": "Proyecto no encontrado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            counterpart_execution = CounterpartExecution.objects.filter(
                activity__in=activities
            ).values_list("id", flat=True)

            movements = MovementsCounterpart.objects.filter(
                counterpart_execution_id__in=counterpart_execution
            )

            total_amount = movements.aggregate(Sum("amount"))["amount__sum"] or 0

            return Response({"total_amount": total_amount}, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error obteniendo la suma de los movimientos: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
