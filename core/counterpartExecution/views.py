from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CounterpartExecutionSerializer
from .models import CounterpartExecution
from core.counterparts.models import Counterpart
from core.activities.models import Activity
from core.movementsCounterpart.models import MovementsCounterpart

# Create your views here.
counter_execution_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "number": openapi.Schema(
            type=openapi.TYPE_STRING, description="Número de la ejecución contrapartida"
        ),
        "expedition_date": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATE,
            description="Fecha de expedición",
        ),
        "amount": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="Monto de la ejecución contrapartida"
        ),
        "description": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Descripciónde la ejecución contrapartida",
        ),
        "is_generated": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Indica si la ejecución contrapartida fue generada",
        ),
        "is_canceled": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Indica si la ejecución contrapartida fue cancelada",
        ),
        "counterpart_id": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="ID de la contrapartida asociado a la ejecución",
        ),
        "activity_id": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="ID de la actividad asociada a la ejecución",
        ),
    },
)


class CounterpartExecutionView(APIView):
    """
    Class to handle HTTP requests related to Counterpart Execution

    @Methods
    - get: Get all counterpart executions
    - post: Create a new counterpart execution
    """

    @swagger_auto_schema(
        operation_description="Obtener todas las ejecuciones de contrapartida",
        responses={
            200: openapi.Schema(
                description="Lista de ejecuciones de contrapartida",
                schema=CounterpartExecutionSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):
        """
        Get all counterpart executions
        @param request: HTTP request
        @return:  JSON response
        """
        try:
            counterpart_executions = CounterpartExecution.objects.all()
            serializer = CounterpartExecutionSerializer(
                counterpart_executions, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error al obtener las ejecuciones de contrapartida: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Crear una nueva ejecución de contrapartida",
        request_body=counter_execution_request_body,
        responses={
            201: openapi.Response(description="Ejecución de contrapartida creada"),
            400: openapi.Response(description="Contrapartida no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):
        """
        Create a new counterpart execution
        @param request: HTTP request
        @return: JSON response
        """
        try:
            data = request.data
            counterpart = Counterpart.objects.get(id=data["counterpart_id"])
            activity = Activity.objects.get(id=data["activity_id"])

            counterpart_execution = CounterpartExecution.objects.create(
                number=data["number"],
                expedition_date=data["expedition_date"],
                amount=data["amount"],
                description=data["description"],
                is_generated=data["is_generated"],
                is_canceled=data["is_canceled"],
                counterpart_id=counterpart,
                activity_id=activity,
            )

            counterpart_execution = CounterpartExecutionSerializer(
                counterpart_execution, many=False
            )

            movement_counterpart = MovementsCounterpart.objects.create(
                amount=data["amount"],
                description=data["description"],
                type="I",
                counterpart_execution_id=counterpart_execution.id,
            )

            movement_counterpart = CounterpartExecutionSerializer(
                movement_counterpart, many=False
            )

            return Response(counterpart_execution.data, status=status.HTTP_201_CREATED)
        except Counterpart.DoesNotExist:
            response = {
                "message": "Contrapartida no encontrada",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Activity.DoesNotExist:
            response = {
                "message": "Actividad no encontrada",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error al crear la ejecución de contrapartida: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CounterpartExecutionDetailView(APIView):
    """
    Class to handle HTTP requests related to Counterpart Execution

    @Methods
    - get: Get a specific counterpart execution
    - put: Update a specific counterpart execution
    - delete: Delete a specific counterpart execution
    """

    @swagger_auto_schema(
        operation_description="Obtener una ejecución de contrapartida específica",
        responses={
            200: openapi.Schema(
                description="Ejecución de contrapartida",
                schema=CounterpartExecutionSerializer,
            ),
            404: openapi.Response(
                description="Ejecución de contrapartida no encontrada"
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, id):
        """
        Get a specific counterpart execution
        @param request: HTTP request
        @param id: Counterpart execution ID
        @return: JSON response
        """
        try:
            counterpart_execution = CounterpartExecution.objects.get(id=id)
            serializer = CounterpartExecutionSerializer(counterpart_execution)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CounterpartExecution.DoesNotExist:
            response = {
                "message": "Ejecución de contrapartida no encontrada",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error al obtener la ejecución de contrapartida: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Actualizar una ejecución de contrapartida específica",
        request_body=movement_request_body,
        responses={
            200: openapi.Response(description="Ejecución de contrapartida actualizada"),
            404: openapi.Response(
                description="Ejecución de contrapartida no encontrada"
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def put(self, request, id):
        """
        Update a specific counterpart execution
        @param request: HTTP request
        @param id: Counterpart execution ID
        @return: JSON response
        """
        try:
            data = request.data
            counterpart_execution = CounterpartExecution.objects.get(id=id)

            if data.get("counterpart_id"):
                counterpart = Counterpart.objects.get(id=data["counterpart_id"])
                counterpart_execution.counterpart_id = counterpart

            if data.get("activity_id"):
                activity = Activity.objects.get(id=data["activity_id"])
                counterpart_execution.activity_id = activity

            counterpart_execution.number = data.get(
                "number", counterpart_execution.number
            )
            counterpart_execution.expedition_date = data.get(
                "expedition_date", counterpart_execution.expedition_date
            )
            counterpart_execution.amount = data.get(
                "amount", counterpart_execution.amount
            )
            counterpart_execution.description = data.get(
                "description", counterpart_execution.description
            )
            counterpart_execution.is_generated = data.get(
                "is_generated", counterpart_execution.is_generated
            )
            counterpart_execution.is_canceled = data.get(
                "is_canceled", counterpart_execution.is_canceled
            )

            counterpart_execution.save()
            serializer = CounterpartExecutionSerializer(counterpart_execution)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CounterpartExecution.DoesNotExist:
            response = {
                "message": "Ejecución de contrapartida no encontrada",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Counterpart.DoesNotExist:
            response = {
                "message": "Contrapartida no encontrada",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Activity.DoesNotExist:
            response = {
                "message": "Actividad no encontrada",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error al actualizar la ejecución de contrapartida: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Eliminar una ejecución de contrapartida específica",
        responses={
            200: openapi.Response(description="Ejecución de contrapartida eliminada"),
            404: openapi.Response(
                description="Ejecución de contrapartida no encontrada"
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def delete(self, request, id):
        """
        Delete a specific counterpart execution
        @param request: HTTP request
        @param id: Counterpart execution ID
        @return: JSON response
        """
        try:
            counterpart_execution = CounterpartExecution.objects.get(id=id)
            counterpart_execution.delete()
            return Response(
                {"message": "Ejecución de contrapartida eliminada"},
                status=status.HTTP_200_OK,
            )
        except CounterpartExecution.DoesNotExist:
            response = {
                "message": "Ejecución de contrapartida no encontrada",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error al eliminar la ejecución de contrapartida: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CounterpartExecutionsByProjectId(APIView):
    """
    Class to handle HTTP requests related to counterpart executions

    @Methods
    - get: Get all counterpart executions by project ID
    """

    @swagger_auto_schema(
        operation_description="Obtener todas las ejecuciones de contrapartida por ID de proyecto",
        responses={
            200: openapi.Schema(
                description="Lista de ejecuciones de contrapartida",
                schema=CounterpartExecutionSerializer(many=True),
            ),
            400: openapi.Response(description="Proyecto no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, project_id):
        """
        Get all counterpart executions by project ID
        @param request: HTTP request
        @param project_id: Project ID
        @return: JSON response
        """
        try:
            activities = Activity.objects.filter(project_id=project_id)

            if not activities.exists():
                response = {
                    "message": "Proyecto no encontrado",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            counterpart_executions = CounterpartExecution.objects.filter(
                activity__in=activities
            )
            serializer = CounterpartExecutionSerializer(
                counterpart_executions, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error al obtener las ejecuciones de contrapartida por proyecto: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
