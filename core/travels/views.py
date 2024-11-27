from rest_framework import status
from rest_framework.response import Response
from .models import Travel
from rest_framework.views import APIView
from .serializers import TravelSerializer
from core.rubros.models import Rubro
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Definir el cuerpo de la solicitud para el POST de Travel
travel_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "origin": openapi.Schema(
            type=openapi.TYPE_STRING, description="Origen del viaje"
        ),
        "destination": openapi.Schema(
            type=openapi.TYPE_STRING, description="Destino del viaje"
        ),
        "transport": openapi.Schema(
            type=openapi.TYPE_STRING, description="Medio de transporte utilizado"
        ),
        "quantity": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Cantidad de unidades"
        ),
        "cant_persons": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Número de personas"
        ),
        "cant_days": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Número de días"
        ),
        "total": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="Total del viaje"
        ),
        "rubro_id": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID del Rubro asociado al viaje"
        ),
    },
)


class TravelView(APIView):
    # Documentar el método GET para obtener todos los viajes
    @swagger_auto_schema(
        operation_description="Obtener todos los viajes",
        responses={
            200: openapi.Response(
                description="Viajes recuperados correctamente",
                schema=TravelSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):
        try:
            data = Travel.objects.all()
            travel_serializer = TravelSerializer(data, many=True)
            response = {
                "message": "Travels retrieved successfully",
                "status": status.HTTP_200_OK,
                "travels": travel_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving travels: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método POST para crear un nuevo viaje
    @swagger_auto_schema(
        operation_description="Crear un nuevo viaje",
        request_body=travel_request_body,
        responses={
            201: openapi.Response(
                description="Viaje creado correctamente", schema=TravelSerializer
            ),
            400: openapi.Response(description="Rubro no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):
        try:
            data = request.data
            rubro = Rubro.objects.get(id=data["rubro_id"])
            travel = Travel.objects.create(
                origin=data["origin"],
                destination=data["destination"],
                transport=data["transport"],
                quantity=data["quantity"],
                cant_persons=data["cant_persons"],
                cant_days=data["cant_days"],
                total=data["total"],
                rubro_id=rubro,
            )
            travel_serializer = TravelSerializer(travel, many=False)
            response = {
                "message": "Travel created successfully",
                "status": status.HTTP_201_CREATED,
                "travel": travel_serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Rubro.DoesNotExist:
            response = {
                "message": "Rubro does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error creating travel: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TravelDetailView(APIView):
    # Documentar el método GET para obtener un viaje específico por ID
    @swagger_auto_schema(
        operation_description="Obtener un viaje específico por ID",
        responses={
            200: openapi.Response(
                description="Viaje recuperado correctamente", schema=TravelSerializer
            ),
            400: openapi.Response(description="Viaje no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, pk):
        try:
            travel = Travel.objects.get(id=pk)
            travel_serializer = TravelSerializer(travel, many=False)
            response = {
                "message": "Travel retrieved successfully",
                "status": status.HTTP_200_OK,
                "travel": travel_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Travel.DoesNotExist:
            response = {
                "message": "Travel does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error retrieving travel: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
