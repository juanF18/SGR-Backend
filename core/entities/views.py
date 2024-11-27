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
        "description": openapi.Schema(
            type=openapi.TYPE_STRING, description="Descripción de la entidad"
        ),
        "address": openapi.Schema(
            type=openapi.TYPE_STRING, description="Dirección de la entidad"
        ),
        "phone": openapi.Schema(
            type=openapi.TYPE_STRING, description="Teléfono de la entidad"
        ),
        "email": openapi.Schema(
            type=openapi.TYPE_STRING, description="Correo electrónico de la entidad"
        ),
        "city": openapi.Schema(
            type=openapi.TYPE_STRING, description="Ciudad de la entidad"
        ),
    },
)


class EntityView(APIView):
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
        try:
            entities = Entity.objects.all()
            entity_serializer = EntitySerializer(entities, many=True)
            response = {
                "message": "Entities retrieved successfully",
                "status": status.HTTP_200_OK,
                "entities": entity_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving entities: {str(e)}",
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
        try:
            data = request.data
            entity_validator = EntityValidator(data)
            if not entity_validator.is_valid():
                response = {
                    "message": "Invalid data",
                    "errors": entity_validator.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            entity = Entity.objects.create(
                name=data["name"],
                description=data["description"],
                address=data["address"],
                phone=data["phone"],
                email=data["email"],
            )
            entity_serializer = EntitySerializer(entity, many=False)
            response = {
                "message": "Entity created successfully",
                "status": status.HTTP_201_CREATED,
                "entity": entity_serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                "message": f"Error creating entity: {str(e)}",
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
            response = {
                "message": "Entity updated successfully",
                "status": status.HTTP_200_OK,
                "entity": entity_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Entity.DoesNotExist:
            response = {
                "message": "Entity not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error updating entity: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EntityDetailView(APIView):
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
        try:
            entity = Entity.objects.get(id=id)
            entity_serializer = EntitySerializer(entity, many=False)
            response = {
                "message": "Entity retrieved successfully",
                "status": status.HTTP_200_OK,
                "entity": entity_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Entity.DoesNotExist:
            response = {
                "message": "Entity not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error retrieving entity: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
