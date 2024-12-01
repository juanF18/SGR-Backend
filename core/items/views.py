from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer
from core.rubros.models import Rubro
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Definir el cuerpo de la solicitud para el POST en ItemView
item_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "description": openapi.Schema(
            type=openapi.TYPE_STRING, description="Descripción del item"
        ),
        "justificacion": openapi.Schema(
            type=openapi.TYPE_STRING, description="Justificación del item"
        ),
        "quantity": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Cantidad del item"
        ),
        "unit_value": openapi.Schema(
            type=openapi.TYPE_NUMBER,
            format=openapi.FORMAT_FLOAT,
            description="Valor unitario del item",
        ),
        "total_value": openapi.Schema(
            type=openapi.TYPE_NUMBER,
            format=openapi.FORMAT_FLOAT,
            description="Valor total del item",
        ),
        "rubro_id": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="ID del rubro relacionado con el item",
        ),
    },
)


class ItemView(APIView):

    """
    Class to handle HTTP requests related to items

    @methods:
    - get: Get all items
    - post: Create a new item
    """

    # Documentar el método GET para obtener todos los items
    @swagger_auto_schema(
        operation_description="Obtener todos los items",
        responses={
            200: openapi.Response(
                description="Items recuperados correctamente",
                schema=ItemSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):

        """
        Get all items
        @param request: HTTP request
        @return: JSON response
        """

        try:
            items = Item.objects.all()
            item_serializer = ItemSerializer(items, many=True)

            return Response(item_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving items: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método POST para crear un item
    @swagger_auto_schema(
        operation_description="Crear un nuevo item",
        request_body=item_request_body,
        responses={
            201: openapi.Response(
                description="Item creado correctamente", schema=ItemSerializer
            ),
            400: openapi.Response(description="Rubro no existe"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):

        """
        Create a new item
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = request.data
            rubro = Rubro.objects.get(id=data["rubro_id"])
            item = Item.objects.create(
                description=data["description"],
                justificacion=data["justificacion"],
                quantity=data["quantity"],
                unit_value=data["unit_value"],
                total_value=data["total_value"],
                rubro_id=rubro,
            )
            item_serializer = ItemSerializer(item)

            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        except Rubro.DoesNotExist:
            response = {
                "message": "Rubro does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error creating item: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ItemDetailView(APIView):

    """
    Class to handle HTTP requests related to a specific item

    @methods:
    - get: Get a specific item by ID
    """
    
    # Documentar el método GET para obtener un item específico por ID
    @swagger_auto_schema(
        operation_description="Obtener un item específico por ID",
        responses={
            200: openapi.Response(
                description="Item recuperado correctamente", schema=ItemSerializer
            ),
            400: openapi.Response(description="Item no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            item_serializer = ItemSerializer(item)

            return Response(item_serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            response = {
                "message": "Item does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error retrieving item: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
