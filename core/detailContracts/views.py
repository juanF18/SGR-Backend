from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DetailContract
from .serializers import DetailContractSerializer
from core.contracts.models import Contract
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Definir el cuerpo de la solicitud para el POST en DetailContractView
detail_contract_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "description": openapi.Schema(
            type=openapi.TYPE_STRING, description="Descripción del contrato"
        ),
        "start_date": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            description="Fecha de inicio",
        ),
        "end_date": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            description="Fecha de fin",
        ),
        "state": openapi.Schema(
            type=openapi.TYPE_STRING, description="Estado del contrato"
        ),
        "task_id": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID de la tarea relacionada"
        ),
        "contract_id": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID del contrato relacionado"
        ),
    },
)


class DetailContractView(APIView):

    """
    Class to handle HTTP requests related to detail contracts

    @methods:
    - get: Get all detail contracts
    - post: Create a new detail contract
    """

    # Documentar el método GET para obtener todos los detalles de contratos
    @swagger_auto_schema(
        operation_description="Obtener todos los detalles de los contratos",
        responses={
            200: openapi.Response(
                description="Detalles de contratos recuperados correctamente",
                schema=DetailContractSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):

        """
        Get all detail contracts
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = DetailContract.objects.all()
            detail_contract_serializer = DetailContractSerializer(data, many=True)

            return Response(detail_contract_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving detail contracts: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método POST para crear un detalle de contrato
    @swagger_auto_schema(
        operation_description="Crear un detalle de contrato",
        request_body=detail_contract_request_body,
        responses={
            201: openapi.Response(
                description="Detalle de contrato creado correctamente",
                schema=DetailContractSerializer,
            ),
            400: openapi.Response(description="Contrato no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):

        """
        Create a new detail contract
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = request.data
            contract = Contract.objects.get(id=data["contract_id"])
            detail_contract = DetailContract.objects.create(
                description=data["description"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                state=data["state"],
                task_id=data["task_id"],
                contract_id=contract,
            )
            detail_contract_serializer = DetailContractSerializer(
                detail_contract, many=False
            )

            return Response(detail_contract_serializer.data, status=status.HTTP_201_CREATED)
        except Contract.DoesNotExist:
            response = {
                "message": "Contract does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error creating detail contract: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DetailContractDetailView(APIView):

    """
    Class to handle HTTP requests related to a specific detail contract

    @methods:
    - get: Get a detail contract by ID
    """

    # Documentar el método GET para obtener un detalle de contrato por ID
    @swagger_auto_schema(
        operation_description="Obtener detalles de un contrato específico por ID",
        responses={
            200: openapi.Response(
                description="Detalle de contrato recuperado correctamente",
                schema=DetailContractSerializer,
            ),
            400: openapi.Response(description="Detalle de contrato no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, id):

        """
        Get a detail contract by ID
        @param request: HTTP request
        @param id: Detail contract ID
        @return: JSON response
        """

        try:
            data = DetailContract.objects.get(id=id)
            detail_contract_serializer = DetailContractSerializer(data, many=False)

            return Response(detail_contract_serializer.data, status=status.HTTP_200_OK)
        except DetailContract.DoesNotExist:
            response = {
                "message": "Detail contract does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error retrieving detail contract: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
