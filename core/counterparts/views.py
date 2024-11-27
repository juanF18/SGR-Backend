from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Counterpart
from .serializers import CounterpartSerializer
from core.rubros.models import Rubro
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Definir el cuerpo de la solicitud para el POST en CounterpartView
counterpart_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(
            type=openapi.TYPE_STRING, description="Nombre de la contraparte"
        ),
        "value_species": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="Valor en especie"
        ),
        "value_chash": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="Valor en efectivo"
        ),
        "rubro_id": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID del rubro relacionado"
        ),
    },
)


class CounterpartView(APIView):

    """
    Class to handle HTTP requests related to counterparts

    @methods:
    - get: Get all counterparts
    - post: Create a new counterpart
    """

    # Documentar el método GET para obtener todas las contrapartes
    @swagger_auto_schema(
        operation_description="Obtener todas las contrapartes",
        responses={
            200: openapi.Response(
                description="Contrapartes recuperadas correctamente",
                schema=CounterpartSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):

        """
        Get all counterparts
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = Counterpart.objects.all()
            counterpart_serializer = CounterpartSerializer(data, many=True)
        
            return Response(counterpart_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving counterparts: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método POST para crear una nueva contraparte
    @swagger_auto_schema(
        operation_description="Crear una nueva contraparte",
        request_body=counterpart_request_body,
        responses={
            201: openapi.Response(
                description="Contraparte creada correctamente",
                schema=CounterpartSerializer,
            ),
            400: openapi.Response(description="Rubro no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):

        """
        Create a new counterpart
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = request.data
            rubro = Rubro.objects.get(id=data["rubro_id"])
            counterpart = Counterpart.objects.create(
                name=data["name"],
                value_species=data["value_species"],
                value_chash=data["value_chash"],
                rubro_id=rubro,
            )
            counterpart_serializer = CounterpartSerializer(counterpart, many=False)

            return Response(counterpart_serializer.data, status=status.HTTP_201_CREATED)
        except Rubro.DoesNotExist:
            response = {
                "message": "Rubro does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error creating counterpart: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CounterpartDetailView(APIView):

    """
    Class to handle HTTP requests related to a single counterpart

    @methods:
    - get: Get a counterpart by ID
    """

    # Documentar el método GET para obtener los detalles de una contraparte
    @swagger_auto_schema(
        operation_description="Obtener los detalles de una contraparte",
        responses={
            200: openapi.Response(
                description="Contraparte recuperada correctamente",
                schema=CounterpartSerializer,
            ),
            400: openapi.Response(description="Contraparte no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, id):

        """
        Get a counterpart by ID
        @param request: HTTP request
        @param id: Counterpart ID
        @return: JSON response
        """

        try:
            counterpart = Counterpart.objects.get(id=id)
            counterpart_serializer = CounterpartSerializer(counterpart, many=False)

            return Response(counterpart_serializer.data, status=status.HTTP_200_OK)
        except Counterpart.DoesNotExist:
            response = {
                "message": "Counterpart does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error retrieving counterpart: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
