from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from .models import Project
from .serializers import ProjectSerializer, ProjectValidator, ProjectFileSerializer
from .utils import (
    BudgetProcessor,
    ActivitiesProcessor,
    InvalidFileFormatError,
    DatabaseError,
)
from core.entities.models import Entity
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
            format=openapi.FORMAT_DATE,
            description="Fecha de inicio del proyecto (YYYY-MM-DD)",
        ),
        "end_date": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATE,
            description="Fecha de finalización del proyecto (YYYY-MM-DD)",
        ),
        "file_budget": openapi.Schema(
            type=openapi.TYPE_FILE,
            description="Archivo de presupuesto en formato .xlsx",
        ),
        "file_activities": openapi.Schema(
            type=openapi.TYPE_FILE,
            description="Archivo de actividades en formato .xlsx",
        ),
        "entity_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="ID de la entidad asociada"
        ),
    },
    required=["name", "description", "value", "start_date", "end_date", "entity_id"],
)


class ProjectView(APIView):
    """
    Class to handle HTTP requests related to projects

    @methods:
    - get: Get all projects
    - post: Create a new project
    """

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
        """
        Get all projects
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = Project.objects.all()
            project_serializer = ProjectSerializer(
                data, many=True, context={"request": request}
            )

            return Response(project_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving projects: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="Crear un nuevo proyecto",
        request_body=ProjectFileSerializer,
        responses={
            201: openapi.Response(
                description="Proyecto creado correctamente", schema=ProjectSerializer
            ),
            400: openapi.Response(
                description="Datos inválidos para la creación del proyecto"
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
        consumes=["multipart/form-data"],
    )
    def post(self, request):
        """
        Create a new project
        @param request: HTTP request
        @return: JSON response
        """
        try:
            # Obtener los datos del formulario (sin los archivos)
            data = request.data
            entity = (
                Entity.objects.get(id=data["entity_id"])
                if data.get("entity_id")
                else None
            )

            # Validar los datos del proyecto (sin los archivos)
            project_validator = ProjectValidator(data)
            if not project_validator.is_valid():
                response = {
                    "message": "Invalid data for project creation validation",
                    "errors": project_validator.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # Obtener los archivos
            file_budget = request.FILES.get("file_budget")
            file_activities = request.FILES.get("file_activities")

            # Validar los archivos (si se envían)
            if file_budget and not file_budget.name.endswith(".xlsx"):
                return Response(
                    {
                        "message": "El archivo de presupuesto que enviaste no tiene formato válido (.xlsx)"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if file_activities and not file_activities.name.endswith(".xlsx"):
                return Response(
                    {
                        "message": "El archivo de actividades que enviaste no tiene formato válido (.xlsx)"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                # Crear el proyecto
                project = Project.objects.create(
                    name=data["name"],
                    description=data["description"],
                    value=data["value"],
                    start_date=data["start_date"],
                    end_date=data["end_date"],
                    entity=entity,
                )

                # Guardar los archivos, si fueron enviados
                if file_budget:
                    project.file_budget = file_budget
                if file_activities:
                    project.file_activities = file_activities
                project.save()

                # Procesar el archivo de presupuestos
                if file_budget:
                    processor = BudgetProcessor(file_budget, project)
                    processor.process()

                if file_activities:
                    activities_processor = ActivitiesProcessor(file_activities, project)
                    activities_processor.process()

                # Serializar la respuesta
                project_serializer = ProjectSerializer(project, many=False)
                return Response(project_serializer.data, status=status.HTTP_201_CREATED)

        except InvalidFileFormatError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            # Cualquier otro error inesperado
            response = {
                "message": f"Error creating project: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectDetail(APIView):
    """
    Class to handle HTTP requests related to a specific project

    @methods:
    - get: Get a specific project by ID
    - put: Update a specific project by ID
    - delete: Delete a specific project by ID
    """

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
            return Response(project_serializer.data, status=status.HTTP_200_OK)
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

    # Documentar el método PUT para actualizar un proyecto específico
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="Actualizar un proyecto específico por ID",
        request_body=ProjectFileSerializer,
        responses={
            200: openapi.Response(
                description="Proyecto actualizado correctamente",
                schema=ProjectSerializer,
            ),
            400: openapi.Response(
                description="Datos inválidos para la actualización del proyecto"
            ),
            404: openapi.Response(description="Proyecto no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
        consumes=["multipart/form-data"],  # Asegurar que acepta multipart
    )
    def put(self, request, id):
        try:
            # Obtener el proyecto por ID
            project = Project.objects.get(id=id)

            # Obtener los nuevos datos de la solicitud
            data = request.data

            # Usar el ProjectFileSerializer para validar los datos enviados
            serializer = ProjectFileSerializer(data=data, partial=True)

            if not serializer.is_valid():
                return Response(
                    {"message": "Datos inválidos", "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Validar el campo entity_id
            entity_id = data.get("entity_id")
            if entity_id:
                try:
                    entity = Entity.objects.get(id=entity_id)
                except Entity.DoesNotExist:
                    return Response(
                        {
                            "message": "Entidad no encontrada",
                            "status": status.HTTP_404_NOT_FOUND,
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )
                project.entity = entity

            # Actualizar el proyecto con los nuevos datos
            project.name = data.get("name", project.name)
            project.description = data.get("description", project.description)
            project.value = data.get("value", project.value)
            project.start_date = data.get("start_date", project.start_date)
            project.end_date = data.get("end_date", project.end_date)

            # Actualizar archivos si se envían
            if "file_budget" in request.FILES:
                project.file_budget = request.FILES["file_budget"]
            if "file_activities" in request.FILES:
                project.file_activities = request.FILES["file_activities"]

            # Guardar el proyecto actualizado
            project.save()

            # Serializar el proyecto actualizado para la respuesta
            project_serializer = ProjectSerializer(project)

            return Response(project_serializer.data, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            response = {
                "message": "Proyecto no encontrado",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            response = {
                "message": f"Error al actualizar el proyecto: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Eliminar un proyecto específico por ID",
        responses={
            204: openapi.Response(description="Proyecto eliminado correctamente"),
            404: openapi.Response(description="Proyecto no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def delete(self, request, id):
        try:
            # Obtener el proyecto por ID
            project = Project.objects.get(id=id)
            project.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            response = {
                "message": "Project not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error deleting project: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
