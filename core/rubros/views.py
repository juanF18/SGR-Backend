from rest_framework import status
from rest_framework.response import Response
from .models import Rubro
from rest_framework.views import APIView
from .serializers import RubroSerializer
from core.projects.models import Project
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Definir el cuerpo de la solicitud para el POST de Rubro
rubro_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "descripcion": openapi.Schema(
            type=openapi.TYPE_STRING, description="Descripción del rubro"
        ),
        "value_sgr": openapi.Schema(type=openapi.TYPE_NUMBER, description="Valor SGR"),
        "project_id": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID del proyecto asociado"
        ),
    },
)


class RubroView(APIView):

    """
    Class to handle HTTP requests related to rubros

    @methods:
    - get: Get all rubros
    - post: Create a new rubro
    """

    # Documentar el método GET para obtener todos los rubros
    @swagger_auto_schema(
        operation_description="Obtener todos los rubros",
        responses={
            200: openapi.Response(
                description="Rubros recuperados correctamente",
                schema=RubroSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):

        """
        Get all rubros
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = Rubro.objects.all()
            rubro_serializer = RubroSerializer(data, many=True)

            return Response(rubro_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving rubros: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método POST para crear un nuevo rubro
    @swagger_auto_schema(
        operation_description="Crear un nuevo rubro",
        request_body=rubro_request_body,
        responses={
            201: openapi.Response(
                description="Rubro creado correctamente", schema=RubroSerializer
            ),
            400: openapi.Response(
                description="Datos inválidos para la creación del rubro"
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):

        """
        Create a new rubro
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = request.data
            project = Project.objects.get(id=data["project_id"])
            rubro = Rubro.objects.create(
                descripcion=data["descripcion"],
                value_sgr=data["value_sgr"],
                project_id=project,
            )
            rubro_serializer = RubroSerializer(rubro, many=False)

            return Response(rubro_serializer.data, status=status.HTTP_201_CREATED)
        except Project.DoesNotExist:
            response = {
                "message": "Project does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error creating rubro: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RubroDetailView(APIView):

    """
    Class to handle HTTP requests related to a specific rubro

    @methods:
    - get: Get a specific rubro by ID
    """

    # Documentar el método GET para obtener un rubro específico por ID
    @swagger_auto_schema(
        operation_description="Obtener un rubro específico por ID",
        responses={
            200: openapi.Response(
                description="Rubro recuperado correctamente", schema=RubroSerializer
            ),
            400: openapi.Response(description="Rubro no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, pk):

        """
        Get a specific rubro by ID
        @param request: HTTP request
        @param pk: Rubro ID
        @return: JSON response
        """

        try:
            rubro = Rubro.objects.get(id=pk)
            rubro_serializer = RubroSerializer(rubro, many=False)

            return Response(rubro_serializer.data, status=status.HTTP_200_OK)
        except Rubro.DoesNotExist:
            response = {
                "message": "Rubro does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error retrieving rubro: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
