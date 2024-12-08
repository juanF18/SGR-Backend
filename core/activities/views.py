from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Activity
from .serializers import ActivitySerializer
from core.projects.models import Project
from core.rubros.models import Rubro
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Parámetros para el cuerpo de la solicitud POST (Activity)
activity_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(
            type=openapi.TYPE_STRING, description="Nombre de la actividad"
        ),
        "description": openapi.Schema(
            type=openapi.TYPE_STRING, description="Descripción de la actividad"
        ),
        "type": openapi.Schema(
            type=openapi.TYPE_STRING, description="Tipo de actividad"
        ),
        "start_date": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATE,
            description="Fecha de inicio de la actividad",
        ),
        "end_date": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATE,
            description="Fecha de fin de la actividad",
        ),
        "state": openapi.Schema(
            type=openapi.TYPE_STRING, description="Estado de la actividad"
        ),
        "project_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="ID del proyecto relacionado"
        ),
        "rubro_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="ID del rubro relacionado"
        ),
    },
)


class ActivityView(APIView):

    """
    Class to handle the requests related to the activities

    @methods:
    - get: Get all activities
    - post: Create a new activity
    """

    # Documentar el método GET para obtener actividades
    @swagger_auto_schema(
        operation_description="Obtener todas las actividades",
        responses={
            200: openapi.Response(
                description="Actividades recuperadas correctamente",
                schema=ActivitySerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):

        """
        Get all the activities
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = Activity.objects.all()
            activity_serializer = ActivitySerializer(data, many=True)

            return Response(activity_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving activities: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método POST para crear una nueva actividad
    @swagger_auto_schema(
        operation_description="Crear una nueva actividad",
        request_body=activity_request_body,
        responses={
            201: openapi.Response(
                description="Actividad creada correctamente", schema=ActivitySerializer
            ),
            400: openapi.Response(
                description="Error en los datos de entrada (por ejemplo, Proyecto o Rubro no existe)"
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):

        """
        Create a new activity
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = request.data
            project = Project.objects.get(id=data["project_id"])
            rubro = Rubro.objects.get(id=data["rubro_id"])
            activity = Activity.objects.create(
                name=data["name"],
                description=data["description"],
                type=data["type"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                state=data["state"],
                project_id=project,
                rubro_id=rubro,
            )
            activity_serializer = ActivitySerializer(activity, many=False)

            return Response(activity_serializer.data, status=status.HTTP_201_CREATED)
        except Project.DoesNotExist:
            response = {
                "message": "Project does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Rubro.DoesNotExist:
            response = {
                "message": "Rubro does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error creating activity: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ActivityDetailView(APIView):

    """
    Class to handle the requests related to the activity details

    @methods:
    - get: Get a specific activity by ID
    """

    # Documentar el método GET para obtener el detalle de una actividad
    @swagger_auto_schema(
        operation_description="Obtener los detalles de una actividad",
        responses={
            200: openapi.Response(
                description="Actividad recuperada correctamente",
                schema=ActivitySerializer,
            ),
            400: openapi.Response(description="Actividad no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, pk):

        """
        Get a specific activity by ID
        @param request: HTTP request
        @param pk: Activity ID
        @return: JSON response
        """

        try:
            activity = Activity.objects.get(id=pk)
            activity_serializer = ActivitySerializer(activity)

            return Response(activity_serializer.data, status=status.HTTP_200_OK)
        except Activity.DoesNotExist:
            response = {
                "message": "Activity does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error retrieving activity: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
