from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CounterpartExecution
from .serializers import CounterpartExecutionSerializer
from core.movementsCounterpart.models import MovementsCounterparts
from core.counterparts.models import Counterpart
from core.activities.models import Activity
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

execution_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "number": openapi.Schema(
            type=openapi.TYPE_STRING, description="Número de la ejecución"
        ),
        "amount": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="Monto de la ejecución"
        ),
        "description": openapi.Schema(
            type=openapi.TYPE_STRING, description="Descripción de la ejecución"
        ),
        "expedition_date": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATE,
            description="Fecha de expedición",
        ),
        "is_generated": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Indica si la ejecución está generada",
        ),
        "is_canceled": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Indica si la ejecución está cancelada",
        ),
        "counterpart_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="ID de la contraparte asociada"
        ),
        "activity_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="ID de la actividad asociada"
        ),
    },
)


class CounterpartExecutionView(APIView):
    """
    Class to handle HTTP requests related to CounterpartExecution
    """

    @swagger_auto_schema(
        operation_description="Obtener todas las ejecuciones de contrapartidas",
        responses={
            200: openapi.Response(
                description="Ejecuciones recuperadas correctamente",
                schema=CounterpartExecutionSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):
        try:
            executions = CounterpartExecution.objects.all()
            serializer = CounterpartExecutionSerializer(executions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": f"Error al obtener las ejecuciones: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Crear una nueva ejecución de contrapartida",
        request_body=execution_request_body,
        responses={
            201: openapi.Response(
                description="Ejecución creada correctamente",
                schema=CounterpartExecutionSerializer,
            ),
            400: openapi.Response(description="Error en los datos de entrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):
        try:
            data = request.data
            counterpart = Counterpart.objects.get(id=data["counterpart_id"])
            activity = Activity.objects.get(id=data["activity_id"])

            # Crear la ejecución de contraparte
            execution = CounterpartExecution.objects.create(
                number=data["number"],
                amount=data["amount"],
                description=data["description"],
                expedition_date=data["expedition_date"],
                is_generated=data["is_generated"],
                is_canceled=data["is_canceled"],
                counterpart=counterpart,
                activity=activity,
            )

            MovementsCounterparts.objects.create(
                amount=data["amount"],
                description=f"Movimiento asociado a ejecución {execution.number}",
                type="I",
                counterpart_execution_id=execution.id,
            )

            serializer = CounterpartExecutionSerializer(execution)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Counterpart.DoesNotExist:
            return Response(
                {"message": "Contraparte no encontrada"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Activity.DoesNotExist:
            return Response(
                {"message": "Actividad no encontrada"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": f"Error al crear la ejecución: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CounterpartExecutionDetailView(APIView):
    """
    Class to handle specific CounterpartExecution requests
    """

    @swagger_auto_schema(
        operation_description="Obtener los detalles de una ejecución específica",
        responses={
            200: openapi.Response(
                description="Ejecución recuperada correctamente",
                schema=CounterpartExecutionSerializer,
            ),
            400: openapi.Response(description="Ejecución no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, execution_id):
        try:
            execution = CounterpartExecution.objects.get(id=execution_id)
            serializer = CounterpartExecutionSerializer(execution)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CounterpartExecution.DoesNotExist:
            return Response(
                {"message": "Ejecución no encontrada"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": f"Error al obtener la ejecución: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Actualizar una ejecución específica por ID",
        request_body=execution_request_body,
        responses={
            200: openapi.Response(
                description="Ejecución actualizada correctamente",
                schema=CounterpartExecutionSerializer,
            ),
            400: openapi.Response(description="Ejecución no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def put(self, request, execution_id):
        try:
            execution = CounterpartExecution.objects.get(id=execution_id)
            data = request.data

            if "counterpart_id" in data:
                execution.counterpart = Counterpart.objects.get(
                    id=data["counterpart_id"]
                )

            if "activity_id" in data:
                execution.activity = Activity.objects.get(id=data["activity_id"])

            execution.number = data.get("number", execution.number)
            execution.amount = data.get("amount", execution.amount)
            execution.description = data.get("description", execution.description)
            execution.expedition_date = data.get(
                "expedition_date", execution.expedition_date
            )
            execution.is_generated = data.get("is_generated", execution.is_generated)
            execution.is_canceled = data.get("is_canceled", execution.is_canceled)

            execution.save()

            serializer = CounterpartExecutionSerializer(execution)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except CounterpartExecution.DoesNotExist:
            return Response(
                {"message": "Ejecución no encontrada"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Counterpart.DoesNotExist:
            return Response(
                {"message": "Contraparte no encontrada"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Activity.DoesNotExist:
            return Response(
                {"message": "Actividad no encontrada"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": f"Error al actualizar la ejecución: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Eliminar una ejecución específica por ID",
        responses={
            200: openapi.Response(description="Ejecución eliminada correctamente"),
            400: openapi.Response(description="Ejecución no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def delete(self, request, execution_id):
        try:
            execution = CounterpartExecution.objects.get(id=execution_id)
            execution.delete()
            return Response(
                {"message": "Ejecución eliminada correctamente"},
                status=status.HTTP_200_OK,
            )
        except CounterpartExecution.DoesNotExist:
            return Response(
                {"message": "Ejecución no encontrada"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": f"Error al eliminar la ejecución: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
