from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserSerializer, UserValidator
from .models import User
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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
            type=openapi.TYPE_INTEGER, description="ID del rol del usuario"
        ),
        "entity_id": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID de la entidad asociada"
        ),
    },
)


# Documentar la vista para obtener todos los usuarios y crear uno nuevo
class UserView(APIView):
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
        try:
            users = User.objects.all()
            user_serializer = UserSerializer(users, many=True)
            response = {
                "message": "Users retrieved successfully",
                "status": status.HTTP_200_OK,
                "users": user_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving users: {str(e)}",
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
        try:
            data = request.data
            user_validator = UserValidator(data)
            if not user_validator.is_valid():
                response = {
                    "message": "Invalid data",
                    "errors": user_validator.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create(
                name=data["name"],
                last_name=data["last_name"],
                email=data["email"],
                identification=data["identification"],
                password=make_password(data["password"]),
                role_id=data["role_id"],
                entity_id=data["entity_id"],
            )
            user_serializer = UserSerializer(user, many=False)
            response = {
                "message": "User created successfully",
                "status": status.HTTP_201_CREATED,
                "user": user_serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                "message": f"Error creating user: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Documentar la vista para obtener un usuario específico
class UserDetailView(APIView):
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
        try:
            user = User.objects.get(id=pk)
            user_serializer = UserSerializer(user, many=False)
            response = {
                "message": "User retrieved successfully",
                "status": status.HTTP_200_OK,
                "user": user_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            response = {
                "message": "User not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error retrieving user: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Documentar la vista para login (obtener token)
class LoginUserView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_description="Iniciar sesión y obtener un token",
        responses={
            200: openapi.Response(
                description="Token obtenido correctamente",
                schema=MyTokenObtainPairSerializer,
            ),
            400: openapi.Response(description="Credenciales incorrectas"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
