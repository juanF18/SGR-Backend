from rest_framework import status
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Counterpart
from .serializers import CounterpartSerializer
from core.projects.models import Project
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
        "project_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="ID del proyecto relacionado"
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
                "message": f"Error obteniendo las contrapartidas: {str(e)}",
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
            project = Project.objects.get(id=data["project_id"])

            counterpart = Counterpart.objects.create(
                name=data["name"],
                value_species=data["value_species"],
                value_chash=data["value_chash"],
                project_id=project.id,
            )
            counterpart_serializer = CounterpartSerializer(counterpart, many=False)

            return Response(counterpart_serializer.data, status=status.HTTP_201_CREATED)
        except Project.DoesNotExist:
            response = {
                "message": "Proyecto no encontrado",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error creando la contrapartida: {str(e)}",
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
                "message": "La contrapartida no existe",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error obteniendo la contrapartida: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Actualizar una contrapartida específica por ID",
        request_body=counterpart_request_body,
        responses={
            200: openapi.Response(
                description="contrapartida actualizada correctamente",
                schema=CounterpartSerializer,
            ),
            400: openapi.Response(description="contrapartida no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def put(self, request, pk):
        """
        Update a counterpart
        @param request: HTTP request
        @param pk: Counterpart ID
        @return: JSON response
        """

        try:
            counterpart = Counterpart.objects.get(id=pk)

            data = request.data

            if data.get("project_id"):
                project = Project.objects.get(id=data["project_id"])
                counterpart.project = project

            counterpart.name = data.get("name", counterpart.name)
            counterpart.value_species = data.get(
                "value_species", counterpart.value_species
            )
            counterpart.value_chash = data.get("value_chash", counterpart.value_chash)

            counterpart.save()

            counterpart_serializer = CounterpartSerializer(counterpart, many=False)

            return Response(counterpart_serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            response = {
                "message": "Proyecto no encontrado",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Counterpart.DoesNotExist:
            response = {
                "message": "Contrapartida no encontrada",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error actualizando contrapartida: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Eliminar una contrapartida específica por ID",
        responses={
            200: openapi.Response(
                description="Contrapartida eliminada correctamente",
                schema=CounterpartSerializer,
            ),
            400: openapi.Response(description="Contrapartida no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def delete(self, request, pk):
        """
        Delete a counterpart
        @param request: HTTP request
        @param pk: Counterpart ID
        @return: JSON response
        """

        try:
            counterpart = Counterpart.objects.get(id=pk)
            counterpart.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Counterpart.DoesNotExist:
            response = {
                "message": "Contrapartida no encontrada",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error eliminando la contrapartida: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CounterpartSumView(APIView):
    """
    Class to handle HTTP requests for summing counterpart values

    @methods:
    - get: Get the total sum of value_species and value_cash for all counterparts
    """

    @swagger_auto_schema(
        operation_description="Obtener la suma total de value_species y value_cash",
        responses={
            200: openapi.Response(
                description="Suma calculada correctamente",
                examples={
                    "application/json": {
                        "total_value_species": 10000.00,
                        "total_value_cash": 15000.00,
                        "total_value_combined": 25000.00,
                    }
                },
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):
        """
        Get the total sum of value_species and value_cash for all counterparts
        @param request: HTTP request
        @return: JSON response with sums
        """
        try:
            total_species = (
                Counterpart.objects.aggregate(Sum("value_species"))[
                    "value_species__sum"
                ]
                or 0
            )
            total_cash = (
                Counterpart.objects.aggregate(Sum("value_chash"))["value_chash__sum"]
                or 0
            )
            total_combined = total_species + total_cash

            response_data = {
                "total_value_species": total_species,
                "total_value_cash": total_cash,
                "total_value_combined": total_combined,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error calculando las sumas: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
