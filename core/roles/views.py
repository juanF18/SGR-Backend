from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Role
from .serializers import RoleSerializer, RoleValidator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Definir el cuerpo de la solicitud para el POST y PUT en RoleView
role_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del rol"),
    },
)


class RoleView(APIView):

    """
    Class to handle HTTP requests related to roles

    @methods:
    - get: Get all roles
    - post: Create a new role
    - put: Update an existing role
    """

    # Documentar el método GET para obtener todos los roles
    @swagger_auto_schema(
        operation_description="Obtener todos los roles",
        responses={
            200: openapi.Response(
                description="Roles recuperados correctamente",
                schema=RoleSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):
        """
        Get all roles
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = Role.objects.all()
            role_serializer = RoleSerializer(data, many=True)
            return Response(role_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving roles: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método POST para crear un nuevo rol
    @swagger_auto_schema(
        operation_description="Crear un nuevo rol",
        request_body=role_request_body,
        responses={
            201: openapi.Response(
                description="Rol creado correctamente", schema=RoleSerializer
            ),
            400: openapi.Response(
                description="Datos inválidos para la creación del rol"
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):

        """
        Create a new role
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = request.data
            role_validator = RoleValidator(data)
            if not role_validator.is_valid():
                response = {
                    "message": "Invalid data for role creation validation",
                    "errors": role_validator.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            role = Role.objects.create(
                name=data["name"],
            )
            role_serializer = RoleSerializer(role, many=False)

            return Response(role_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                "message": f"Error creating role: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método PUT para actualizar un rol existente
    @swagger_auto_schema(
        operation_description="Actualizar un rol existente",
        request_body=role_request_body,
        responses={
            200: openapi.Response(
                description="Rol actualizado correctamente", schema=RoleSerializer
            ),
            400: openapi.Response(
                description="Datos inválidos para la actualización del rol"
            ),
            404: openapi.Response(description="Rol no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def put(self, request, id):

        """
        Update an existing role
        @param request: HTTP request
        @param id: Role ID
        @return: JSON response
        """

        try:
            data = request.data
            role = self.get_object(id)
            role_validator = RoleValidator(data)
            if not role_validator.is_valid():
                response = {
                    "message": "Invalid data",
                    "errors": role_validator.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            role.name = data["name"]
            role.save()
            role_serializer = RoleSerializer(role, many=False)

            return Response(role_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error updating role: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RoleDetailView(APIView):
    # Documentar el método GET para obtener un rol específico por ID
    @swagger_auto_schema(
        operation_description="Obtener un rol específico por ID",
        responses={
            200: openapi.Response(
                description="Rol recuperado correctamente", schema=RoleSerializer
            ),
            404: openapi.Response(description="Rol no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, id):

        """
        Get a specific role by ID
        @param request: HTTP request
        @param id: Role ID
        @return: JSON response
        """

        try:
            role = Role.objects.get(id=id)
            role_serializer = RoleSerializer(role, many=False)

            return Response(role_serializer.data, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            response = {
                "message": "Role not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error retrieving role: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
