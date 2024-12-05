from rest_framework import status
from rest_framework.response import Response
from .models import Cdps
from rest_framework.views import APIView
from .serializers import CdpsSerializer
from core.rubros.models import Rubro
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Definir el cuerpo de la solicitud para el POST
cdps_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "number": openapi.Schema(
            type=openapi.TYPE_STRING, description="Número del CDP"
        ),
        "expedition_date": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATE,
            description="Fecha de expedición",
        ),
        "amount": openapi.Schema(type=openapi.TYPE_NUMBER, description="Monto del CDP"),
        "description": openapi.Schema(
            type=openapi.TYPE_STRING, description="Descripción del CDP"
        ),
        "is_generated": openapi.Schema(
            type=openapi.TYPE_BOOLEAN, description="Indica si el CDP está generado"
        ),
        "is_canceled": openapi.Schema(
            type=openapi.TYPE_BOOLEAN, description="Indica si el CDP está cancelado"
        ),
        "document": openapi.Schema(
            type=openapi.TYPE_STRING, description="Documento asociado al CDP"
        ),
        "rubro_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="ID del Rubro asociado al CDP"
        ),
    },
)


class CdpsView(APIView):

    """
    Class to handle HTTP requests related to Cdps
    
    @methods:
    - get: Get all Cdps
    - post: Create a new CDP
    """
    # Documentar el método GET para obtener todos los CDPs
    @swagger_auto_schema(
        operation_description="Obtener todos los CDPs",
        responses={
            200: openapi.Response(
                description="CDPs recuperados correctamente",
                schema=CdpsSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):

        """
        Get all Cdps
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = Cdps.objects.all()
            cdps_serializer = CdpsSerializer(data, many=True)

            return Response(cdps_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error al obtener los cdps: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método POST para crear un nuevo CDP
    @swagger_auto_schema(
        operation_description="Crear un nuevo CDP",
        request_body=cdps_request_body,
        responses={
            201: openapi.Response(
                description="CDP creado correctamente", schema=CdpsSerializer
            ),
            400: openapi.Response(
                description="Error en los datos de entrada (por ejemplo, Rubro no existe)"
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):

        """
        Create a new CDP
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = request.data
            rubro = Rubro.objects.get(id=data["rubro_id"])
            cdps = Cdps.objects.create(
                number=data["number"],
                expedition_date=data["expedition_date"],
                amount=data["amount"],
                description=data["description"],
                is_generated=data["is_generated"],
                is_canceled=data["is_canceled"],
                document=data["document"],
                rubro_id=rubro,
            )
            cdps_serializer = CdpsSerializer(cdps, many=False)

            return Response(cdps_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                "message": f"Error al crear el cdp: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CdpsDetailView(APIView):

    """
    Class to handle HTTP requests related to a specific CDP

    @methods:
    - get: Get CDP details
    - put: Update a specific CDP
    - delete: Delete a specific CDP
    """

    # Documentar el método GET para obtener el detalle de un CDP
    @swagger_auto_schema(
        operation_description="Obtener los detalles de un CDP",
        responses={
            200: openapi.Response(
                description="CDP recuperado correctamente", schema=CdpsSerializer
            ),
            400: openapi.Response(description="CDP no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, id):

        """
        Get a specific CDP by ID
        @param request: HTTP request
        @param id: CDP ID
        @return: JSON response
        """

        try:
            cdps = Cdps.objects.get(id=id)
            cdps_serializer = CdpsSerializer(cdps, many=False)

            return Response(cdps_serializer.data, status=status.HTTP_200_OK)
        except Cdps.DoesNotExist:
            response = {
                "message": "Cdp no encontrado",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error al obtener el cdp: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Actualizar un CDP específico por ID",
        request_body=cdps_request_body,
        responses={
            200: openapi.Response(
                description="CDP actualizado correctamente", schema=CdpsSerializer
            ),
            400: openapi.Response(description="CDP no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def put(self, request, pk):

        """
        Update a specific CDP by ID
        @param request: HTTP request
        @param id: CDP ID
        @return: JSON response
        """

        try:
            cdp = Cdps.objects.get(id=pk)

            data = request.data

            if data.get("rubro_id"):
                rubro = Rubro.objects.get(id=data["rubro_id"])
                cdp.rubro_id = rubro

            cdp.number = data.get("number", cdp.number)
            cdp.expedition_date = data.get("expedition_date", cdp.expedition_date)
            cdp.amount = data.get("amount", cdp.amount)
            cdp.description = data.get("description", cdp.description)
            cdp.is_generated = data.get("is_generated", cdp.is_generated)
            cdp.is_canceled = data.get("is_canceled", cdp.is_canceled)
            cdp.document = data.get("document", cdp.document)

            cdp.save()
            
            cdps_serializer = CdpsSerializer(cdp, many=False)            

            return Response(cdps_serializer.data, status=status.HTTP_200_OK)
        except Cdps.DoesNotExist:
            response = {
                "message": "Cdp no encontrado",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Rubro.DoesNotExist:
            response = {
                "message": "Rubro no encontrado",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error al actualizar cdp: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Eliminar un CDP específico por ID",
        responses={
            200: openapi.Response(description="CDP eliminado correctamente"),
            400: openapi.Response(description="CDP no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def delete(self, request, pk):

        """
        Delete a specific CDP by ID
        @param request: HTTP request
        @param id: CDP ID
        @return: JSON response
        """

        try:
            cdp = Cdps.objects.get(id=pk)
            cdp.delete()

            response = {
                "message": "Cdps eliminado correctamente",
                "status": status.HTTP_200_OK,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Cdps.DoesNotExist:
            response = {
                "message": "Cdps no existe",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error al eliminar cdp: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
