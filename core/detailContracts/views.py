from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DetailContract
from .serializers import DetailContractSerializer
from core.contracts.models import Contract


class DetailContractView(APIView):

    def get(self, request):
        try:
            data = DetailContract.objects.all()
            detail_contract_serializer = DetailContractSerializer(data, many=True)
            response = {
                "message": "Detail contracts retrieved successfully",
                "status": status.HTTP_200_OK,
                "detail_contracts": detail_contract_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving detail contracts: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
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
            response = {
                "message": "Detail contract created successfully",
                "status": status.HTTP_201_CREATED,
                "detail_contract": detail_contract_serializer.data,
            }

            return Response(response, status=status.HTTP_201_CREATED)
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

    def get(self, request, id):
        try:
            data = DetailContract.objects.get(id=id)
            detail_contract_serializer = DetailContractSerializer(data, many=False)
            response = {
                "message": "Detail contract retrieved successfully",
                "status": status.HTTP_200_OK,
                "detail_contract": detail_contract_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
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
