from rest_framework import status
from rest_framework.response import Response
from .models import Task
from rest_framework.views import APIView
from .serializers import TaskSerializer
from core.activities.models import Activity
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Definir el cuerpo de la solicitud para el POST de Task
task_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(
            type=openapi.TYPE_STRING, description="Nombre de la tarea"
        ),
        "description": openapi.Schema(
            type=openapi.TYPE_STRING, description="Descripción de la tarea"
        ),
        "state": openapi.Schema(
            type=openapi.TYPE_STRING, description="Estado de la tarea"
        ),
        "activity_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="ID de la actividad asociada"
        ),
    },
)


class TaskView(APIView):
    """
    Class to handle HTTP requests related to tasks

    @methods:
    - get: Get all tasks
    - post: Create a new task
    """

    # Documentar el método GET para obtener todas las tareas
    @swagger_auto_schema(
        operation_description="Obtener todas las tareas",
        responses={
            200: openapi.Response(
                description="Tareas recuperadas correctamente",
                schema=TaskSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):
        """
        Get all tasks
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = Task.objects.all()
            task_serializer = TaskSerializer(data, many=True)

            return Response(task_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error obteniendo las tareas: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método POST para crear una nueva tarea
    @swagger_auto_schema(
        operation_description="Crear una nueva tarea",
        request_body=task_request_body,
        responses={
            201: openapi.Response(
                description="Tarea creada correctamente", schema=TaskSerializer
            ),
            400: openapi.Response(
                description="Datos inválidos para la creación de la tarea"
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):
        """
        Create a new task
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = request.data
            activity = Activity.objects.get(id=data["activity_id"])
            task = Task.objects.create(
                name=data["name"],
                description=data["description"],
                state=data["state"],
                activity_id=activity,
            )
            task_serializer = TaskSerializer(task, many=False)

            return Response(task_serializer.data, status=status.HTTP_201_CREATED)
        except Activity.DoesNotExist:
            response = {
                "message": "Actividad no encontrada",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error creando la tarea: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskDetailView(APIView):
    """
    Class to handle HTTP requests related to a specific task

    @methods:
    - get: Get a specific task by ID
    """

    # Documentar el método GET para obtener una tarea específica por ID
    @swagger_auto_schema(
        operation_description="Obtener una tarea específica por ID",
        responses={
            200: openapi.Response(
                description="Tarea recuperada correctamente", schema=TaskSerializer
            ),
            400: openapi.Response(description="Tarea no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, id):
        """
        Get a specific task by ID
        @param request: HTTP request
        @param id: Task ID
        @return: JSON response
        """

        try:
            task = Task.objects.get(id=id)
            task_serializer = TaskSerializer(task, many=False)

            return Response(task_serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            response = {
                "message": "Tarea no encontrada",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error retrieving task: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Actualizar una tarea específica por ID",
        request_body=task_request_body,
        responses={
            200: openapi.Response(
                description="Tarea actualizada correctamente", schema=TaskSerializer
            ),
            400: openapi.Response(description="Tarea no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def put(self, request, id):
        """
        Update a specific task by ID
        @param request: HTTP request
        @param id: Task ID
        @return: JSON response
        """

        try:
            task = Task.objects.get(id=id)
            data = request.data

            if data.get("activity_id"):
                activity = Activity.objects.get(id=data["activity_id"])
                task.activity = activity

            task.name = data.get("name", task.name)
            task.description = data.get("description", task.description)
            task.state = data.get("state", task.state)
            task.save()

            task_serializer = TaskSerializer(task, many=False)

            return Response(task_serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            response = {
                "message": "Tarea no encontrada",
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
                "message": f"Error actualizando la tarea: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Eliminar una tarea específica por ID",
        responses={
            200: openapi.Response(description="Tarea eliminada correctamente"),
            400: openapi.Response(description="Tarea no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def delete(self, request, pk):
        """
        Delete a specific task by ID
        @param request: HTTP request
        @param id: Task ID
        @return: JSON response
        """

        try:
            task = Task.objects.get(id=pk)
            task.delete()

            response = {
                "message": "Tarea eliminada correctamente",
                "status": status.HTTP_200_OK,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            response = {
                "message": "Tarea no encontrada",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error eliminando la tarea: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
