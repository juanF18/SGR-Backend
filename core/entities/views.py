from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Entity
from .serializers import EntitySerializer, EntityValidator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Definir el cuerpo de la solicitud para el POST y PUT en EntityView
entity_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(
            type=openapi.TYPE_STRING, description="Nombre de la entidad"
        ),
        "nit": openapi.Schema(
            type=openapi.TYPE_STRING, description="Dirección de la entidad"
        ),
        "email": openapi.Schema(
            type=openapi.TYPE_STRING, description="Correo electrónico de la entidad"
        ),
        "phone": openapi.Schema(
            type=openapi.TYPE_STRING, description="Teléfono de la entidad"
        ),
        "address": openapi.Schema(
            type=openapi.TYPE_STRING, description="Dirección de la entidad"
        ),
        "city": openapi.Schema(
            type=openapi.TYPE_STRING, description="Ciudad de la entidad"
        ),
    },
)


class EntityView(APIView):
    """
    Class to handle HTTP requests related to entities

    @methods:
    - get: Get all entities
    - post: Create a new entity
    - put: Update an existing entity
    """

    # Documentar el método GET para obtener todas las entidades
    @swagger_auto_schema(
        operation_description="Obtener todas las entidades",
        responses={
            200: openapi.Response(
                description="Entidades recuperadas correctamente",
                schema=EntitySerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):
        """
        Get all entities
        @param request: HTTP request
        @return: JSON response
        """

        try:
            entities = Entity.objects.all()
            entity_serializer = EntitySerializer(entities, many=True)

            return Response(entity_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error obteniendo las entidades: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método POST para crear una entidad
    @swagger_auto_schema(
        operation_description="Crear una nueva entidad",
        request_body=entity_request_body,
        responses={
            201: openapi.Response(
                description="Entidad creada correctamente", schema=EntitySerializer
            ),
            400: openapi.Response(description="Datos inválidos"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):
        """
        Create a new entity
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = request.data
            print("Esta es la data", data)
            entity_validator = EntityValidator(data)
            if not entity_validator.is_valid():
                response = {
                    "message": "Información inválida",
                    "errors": entity_validator.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            entity = Entity.objects.create(
                name=data["name"],
                nit=data["nit"],
                email=data["email"],
                phone=data["phone"],
                address=data["address"],
                city=data["city"],
            )
            entity_serializer = EntitySerializer(entity, many=False)

            return Response(entity_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                "message": f"Error creando la entidad: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EntityDetailView(APIView):
    """
    Class to handle HTTP requests related to a specific entity

    @methods:
    - get: Get a specific entity by ID
    """

    # Documentar el método GET para obtener una entidad específica por ID
    @swagger_auto_schema(
        operation_description="Obtener una entidad específica por ID",
        responses={
            200: openapi.Response(
                description="Entidad recuperada correctamente", schema=EntitySerializer
            ),
            404: openapi.Response(description="Entidad no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, id):
        """
        Get a specific entity by ID
        @param request: HTTP request
        @param id: Entity ID
        @return: JSON response
        """

        try:
            entity = Entity.objects.get(id=id)
            entity_serializer = EntitySerializer(entity, many=False)

            return Response(entity_serializer.data, status=status.HTTP_200_OK)
        except Entity.DoesNotExist:
            response = {
                "message": "Entidad no encontrada",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error obteniendo la entidad: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método PUT para actualizar una entidad
    @swagger_auto_schema(
        operation_description="Actualizar una entidad existente",
        request_body=entity_request_body,
        responses={
            200: openapi.Response(
                description="Entidad actualizada correctamente", schema=EntitySerializer
            ),
            404: openapi.Response(description="Entidad no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def put(self, request, id):
        """
        Update an existing entity
        @param request: HTTP request
        @param id: Entity ID
        @return: JSON response
        """

        try:
            entity = Entity.objects.get(id=id)
            data = request.data
            entity.name = data["name"]
            entity.email = data["email"]
            entity.phone = data["phone"]
            entity.address = data["address"]
            entity.city = data["city"]
            entity.save()
            entity_serializer = EntitySerializer(entity, many=False)

            return Response(entity_serializer.data, status=status.HTTP_200_OK)
        except Entity.DoesNotExist:
            response = {
                "message": "Entidad no encontrada",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error updating entity: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    """
    Class to handle HTTP requests related to a specific entity

    @methods:
    - get: Get a specific entity by ID
    - delete: Delete a specific entity by ID
    """

    # Documentar el método DELETE para eliminar una entidad específica por ID
    @swagger_auto_schema(
        operation_description="Eliminar una entidad específica por ID",
        responses={
            204: openapi.Response(description="Entidad eliminada correctamente"),
            404: openapi.Response(description="Entidad no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def delete(self, request, id):
        """
        Delete a specific entity by ID
        @param request: HTTP request
        @param id: Entity ID
        @return: JSON response
        """

        try:
            # Buscar la entidad por ID
            entity = Entity.objects.get(id=id)

            # Eliminar la entidad
            entity.delete()

            # Respuesta de éxito sin contenido
            return Response(
                {"message": "Entidad eliminada correctamente"},
                status=status.HTTP_204_NO_CONTENT,
            )

        except Entity.DoesNotExist:
            # Respuesta si la entidad no existe
            return Response(
                {"message": "Entity not found", "status": status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            # Respuesta en caso de error interno
            return Response(
                {
                    "message": f"Error deleting entity: {str(e)}",
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
