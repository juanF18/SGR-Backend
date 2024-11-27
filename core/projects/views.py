from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Project
from .serializers import ProjectSerializer, ProjectValidator
from core.entities.models import Entity
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Definir el cuerpo de la solicitud para el POST en ProjectView
project_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(
            type=openapi.TYPE_STRING, description="Nombre del proyecto"
        ),
        "description": openapi.Schema(
            type=openapi.TYPE_STRING, description="Descripción del proyecto"
        ),
        "value": openapi.Schema(
            type=openapi.TYPE_NUMBER,
            format=openapi.FORMAT_FLOAT,
            description="Valor del proyecto",
        ),
        "start_date": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            description="Fecha de inicio del proyecto",
        ),
        "end_date": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            description="Fecha de finalización del proyecto",
        ),
        "file_budget_url": openapi.Schema(
            type=openapi.TYPE_STRING, description="URL del archivo del presupuesto"
        ),
        "file_activities_url": openapi.Schema(
            type=openapi.TYPE_STRING, description="URL del archivo de actividades"
        ),
        "entity_id": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="ID de la entidad asociada al proyecto",
        ),
    },
)


class ProjectView(APIView):
    # Documentar el método GET para obtener todos los proyectos
    @swagger_auto_schema(
        operation_description="Obtener todos los proyectos",
        responses={
            200: openapi.Response(
                description="Proyectos recuperados correctamente",
                schema=ProjectSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):
        try:
            data = Project.objects.all()
            project_serializer = ProjectSerializer(data, many=True)
            response = {
                "message": "Projects retrieved successfully",
                "status": status.HTTP_200_OK,
                "projects": project_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving projects: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método POST para crear un nuevo proyecto
    @swagger_auto_schema(
        operation_description="Crear un nuevo proyecto",
        request_body=project_request_body,
        responses={
            201: openapi.Response(
                description="Proyecto creado correctamente", schema=ProjectSerializer
            ),
            400: openapi.Response(
                description="Datos inválidos para la creación del proyecto"
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):
        try:
            data = request.data
            entity = Entity.objects.get(id=data["entity_id"])
            project_validator = ProjectValidator(data)
            if not project_validator.is_valid():
                response = {
                    "message": "Invalid data for project creation validation",
                    "errors": project_validator.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            project = Project.objects.create(
                name=data["name"],
                description=data["description"],
                value=data["value"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                file_budget_url=data["file_budget_url"],
                file_activities_url=data["file_activities_url"],
                entity_id=entity,
            )
            project_serializer = ProjectSerializer(project, many=False)

            response = {
                "message": "Project created successfully",
                "status": status.HTTP_201_CREATED,
                "project": project_serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                "message": f"Error creating project: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectDetail(APIView):
    # Documentar el método GET para obtener un proyecto específico por ID
    @swagger_auto_schema(
        operation_description="Obtener un proyecto específico por ID",
        responses={
            200: openapi.Response(
                description="Proyecto recuperado correctamente",
                schema=ProjectSerializer,
            ),
            404: openapi.Response(description="Proyecto no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, id):
        try:
            project = Project.objects.get(id=id)
            project_serializer = ProjectSerializer(project, many=False)
            response = {
                "message": "Project retrieved successfully",
                "status": status.HTTP_200_OK,
                "project": project_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            response = {
                "message": "Project not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error retrieving project: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
