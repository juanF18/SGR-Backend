from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserValidator, LoginUserSerializer
from .models import User
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.roles.models import Role
from core.entities.models import Entity


# Definir el cuerpo de la solicitud para la creación de un usuario
user_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(
            type=openapi.TYPE_STRING, description="Nombre del usuario"
        ),
        "last_name": openapi.Schema(
            type=openapi.TYPE_STRING, description="Apellido del usuario"
        ),
        "email": openapi.Schema(
            type=openapi.TYPE_STRING, description="Correo electrónico del usuario"
        ),
        "identification": openapi.Schema(
            type=openapi.TYPE_STRING, description="Identificación del usuario"
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING, description="Contraseña del usuario"
        ),
        "role_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="ID del rol del usuario"
        ),
        "entity_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="ID de la entidad asociada"
        ),
    },
)


# Documentar la vista para obtener todos los usuarios y crear uno nuevo
class UserView(APIView):
    """
    Clase para manejar solicitudes HTTP relacionadas con los usuarios.
    """

    @swagger_auto_schema(
        operation_description="Obtener todos los usuarios",
        responses={
            200: openapi.Response(
                description="Usuarios recuperados correctamente",
                schema=UserSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):
        """
        Obtener todos los usuarios
        """
        try:
            users = User.objects.all()
            user_serializer = UserSerializer(users, many=True)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                "message": f"Error al obtener los usuarios: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Crear un nuevo usuario",
        request_body=user_request_body,
        responses={
            201: openapi.Response(
                description="Usuario creado correctamente", schema=UserSerializer
            ),
            400: openapi.Response(description="Datos de usuario inválidos"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):
        """
        Crear un nuevo usuario
        """
        try:
            data = request.data

            # Validar datos del usuario
            user_validator = UserValidator(data)
            if not user_validator.is_valid():
                response = {
                    "message": "Datos inválidos",
                    "errors": user_validator.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # Obtener role y entity si existen
            role = Role.objects.get(id=data["role_id"]) if data.get("role_id") else None
            entity = (
                Entity.objects.get(id=data["entity_id"])
                if data.get("entity_id")
                else None
            )

            # Crear el usuario
            user = User.objects.create(
                name=data["name"],
                last_name=data["last_name"],
                email=data["email"],
                identification=data["identification"],
                role=role,
                entity=entity,
            )
            user.set_password(
                data["password"]
            )  # Usamos el método set_password para asegurar el hash
            user.save()

            # Serializar el usuario creado
            user_serializer = UserSerializer(user, many=False)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                "message": f"Error al crear el usuario: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Documentar la vista para obtener un usuario específico y eliminarlo
class UserDetailView(APIView):
    """
    Clase para manejar solicitudes HTTP relacionadas con un usuario específico.
    """

    @swagger_auto_schema(
        operation_description="Obtener un usuario específico por ID",
        responses={
            200: openapi.Response(
                description="Usuario recuperado correctamente", schema=UserSerializer
            ),
            404: openapi.Response(description="Usuario no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, pk):
        """
        Obtener un usuario específico por ID
        """
        try:
            user = User.objects.get(id=pk)
            user_serializer = UserSerializer(user, many=False)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            response = {
                "message": "Usuario no encontrado",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error al obtener el usuario: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Eliminar un usuario específico por ID",
        responses={
            204: openapi.Response(description="Usuario eliminado correctamente"),
            404: openapi.Response(description="Usuario no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def delete(self, request, pk):
        """
        Eliminar un usuario específico por ID
        """
        try:
            user = User.objects.get(id=pk)
            user.delete()
            return Response(
                {"message": "Usuario eliminado correctamente"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except User.DoesNotExist:
            response = {
                "message": "Usuario no encontrado",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error al eliminar el usuario: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Actualizar un usuario específico por ID",
        request_body=user_request_body,
        responses={
            200: openapi.Response(
                description="Usuario actualizado correctamente", schema=UserSerializer
            ),
            400: openapi.Response(description="Datos de usuario inválidos"),
            404: openapi.Response(description="Usuario no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def put(self, request, pk):
        """
        Actualizar un usuario específico por ID
        """
        try:
            # Obtener el usuario que se desea actualizar
            user = User.objects.get(id=pk)

            # Validar los datos del usuario
            data = request.data
            user_validator = UserValidator(data)
            if not user_validator.is_valid():
                response = {
                    "message": "Datos inválidos",
                    "errors": user_validator.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # Si se proporciona un nuevo rol, obtenerlo
            if data.get("role_id"):
                role = Role.objects.get(id=data["role_id"])
                user.role = role

            # Si se proporciona una nueva entidad, obtenerla
            if data.get("entity_id"):
                entity = Entity.objects.get(id=data["entity_id"])
                user.entity = entity

            # Actualizar los campos del usuario
            user.name = data.get("name", user.name)
            user.last_name = data.get("last_name", user.last_name)
            user.email = data.get("email", user.email)
            user.identification = data.get("identification", user.identification)

            # Si se proporciona una nueva contraseña, actualizarla
            if data.get("password"):
                user.set_password(data["password"])

            # Guardar los cambios
            user.save()

            # Serializar el usuario actualizado
            user_serializer = UserSerializer(user, many=False)

            return Response(user_serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            response = {
                "message": "Usuario no encontrado",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error al actualizar el usuario: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Definir el cuerpo de la solicitud para el login
login_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(
            type=openapi.TYPE_STRING, description="Correo electrónico del usuario"
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING, description="Contraseña del usuario"
        ),
    },
)


class LoginUserView(APIView):
    """
    Vista para manejar el login de usuario y la generación de tokens.
    """

    @swagger_auto_schema(
        operation_description="Iniciar sesión y obtener un token",
        request_body=login_request_body,
        responses={
            200: openapi.Response(
                description="Token obtenido correctamente", schema=LoginUserSerializer
            ),
            400: openapi.Response(description="Credenciales incorrectas"),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Método para manejar el login de un usuario
        """
        # Usamos el nuevo serializer
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
