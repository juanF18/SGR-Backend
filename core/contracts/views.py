from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Contract
from .serializers import ContractSerializer
from core.cdps.models import Cdps
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Definir el cuerpo de la solicitud para el POST en ContractView
contract_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "contract_number": openapi.Schema(
            type=openapi.TYPE_STRING, description="Número del contrato"
        ),
        "contracting_nit": openapi.Schema(
            type=openapi.TYPE_STRING, description="NIT del contratante"
        ),
        "contracted_nit": openapi.Schema(
            type=openapi.TYPE_STRING, description="NIT del contratado"
        ),
        "contracting_name": openapi.Schema(
            type=openapi.TYPE_STRING, description="Nombre del contratante"
        ),
        "start_date": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Fecha de inicio del contrato (formato: YYYY-MM-DD)",
        ),
        "end_date": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Fecha de finalización del contrato (formato: YYYY-MM-DD)",
        ),
        "contract_info": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Información adicional sobre el contrato",
        ),
        "amount": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="Monto del contrato"
        ),
        "supervisor_name": openapi.Schema(
            type=openapi.TYPE_STRING, description="Nombre del supervisor"
        ),
        "supervisor_identification": openapi.Schema(
            type=openapi.TYPE_STRING, description="Identificación del supervisor"
        ),
        "contract_url": openapi.Schema(
            type=openapi.TYPE_STRING, description="URL del contrato"
        ),
        "observations": openapi.Schema(
            type=openapi.TYPE_STRING, description="Observaciones del contrato"
        ),
        "cpds_id": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID del CDPS relacionado"
        ),
    },
)


class ContractView(APIView):
    # Documentar el método GET para obtener todos los contratos
    @swagger_auto_schema(
        operation_description="Obtener todos los contratos",
        responses={
            200: openapi.Response(
                description="Contratos recuperados correctamente",
                schema=ContractSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):
        try:
            data = Contract.objects.all()
            contract_serializer = ContractSerializer(data, many=True)
            response = {
                "message": "Contracts retrieved successfully",
                "status": status.HTTP_200_OK,
                "contracts": contract_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving contracts: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método POST para crear un nuevo contrato
    @swagger_auto_schema(
        operation_description="Crear un nuevo contrato",
        request_body=contract_request_body,
        responses={
            201: openapi.Response(
                description="Contrato creado correctamente", schema=ContractSerializer
            ),
            400: openapi.Response(description="CDPS no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):
        try:
            data = request.data
            cpds = Cdps.objects.get(id=data["cpds_id"])
            contract = Contract.objects.create(
                contract_number=data["contract_number"],
                contracting_nit=data["contracting_nit"],
                contracted_nit=data["contracted_nit"],
                contracting_name=data["contracting_name"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                contract_info=data["contract_info"],
                amount=data["amount"],
                supervisor_name=data["supervisor_name"],
                supervisor_identification=data["supervisor_identification"],
                contract_url=data["contract_url"],
                observations=data["observations"],
                cpds_id=cpds,
            )
            contract_serializer = ContractSerializer(contract, many=False)
            response = {
                "message": "Contract created successfully",
                "status": status.HTTP_201_CREATED,
                "contract": contract_serializer.data,
            }

            return Response(response, status=status.HTTP_201_CREATED)
        except Cdps.DoesNotExist:
            response = {
                "message": "Cdps does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error creating contract: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContractDetailView(APIView):
    # Documentar el método GET para obtener los detalles de un contrato
    @swagger_auto_schema(
        operation_description="Obtener los detalles de un contrato",
        responses={
            200: openapi.Response(
                description="Contrato recuperado correctamente",
                schema=ContractSerializer,
            ),
            400: openapi.Response(description="Contrato no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, pk):
        try:
            contract = Contract.objects.get(id=pk)
            response = {
                "message": "Contract retrieved successfully",
                "status": status.HTTP_200_OK,
                "contract": contract,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Contract.DoesNotExist:
            response = {
                "message": "Contract does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error retrieving contract: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
