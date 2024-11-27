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
            type=openapi.TYPE_INTEGER, description="ID del Rubro asociado al CDP"
        ),
    },
)


class CdpsView(APIView):
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
        try:
            data = Cdps.objects.all()
            cdps_serializer = CdpsSerializer(data, many=True)
            response = {
                "message": "Cdps retrieved successfully",
                "status": status.HTTP_200_OK,
                "cdps": cdps_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving cdps: {str(e)}",
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
            response = {
                "message": "Cdps created successfully",
                "status": status.HTTP_201_CREATED,
                "cdps": cdps_serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                "message": f"Error creating cdps: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CdpsDetailView(APIView):
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
        try:
            cdps = Cdps.objects.get(id=id)
            cdps_serializer = CdpsSerializer(cdps, many=False)
            response = {
                "message": "Cdps retrieved successfully",
                "status": status.HTTP_200_OK,
                "cdps": cdps_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Cdps.DoesNotExist:
            response = {
                "message": "Cdps does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error retrieving cdps: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
