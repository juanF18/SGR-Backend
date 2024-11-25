from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Contract
from rest_framework.views import APIView
from .serializers import ContractSerializer
from core.cdps.models import Cdps


# Create your views here.
class ContractView(APIView):
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
