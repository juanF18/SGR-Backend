from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Counterpart
from rest_framework.views import APIView
from .serializers import CounterpartSerializer
from core.rubros.models import Rubro


# Create your views here.
class CounterpartView(APIView):

    def get(self, request):
        try:
            data = Counterpart.objects.all()
            counterpart_serializer = CounterpartSerializer(data, many=True)
            response = {
                "message": "Counterparts retrieved successfully",
                "status": status.HTTP_200_OK,
                "counterparts": counterpart_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving counterparts: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
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
            response = {
                "message": "Counterpart created successfully",
                "status": status.HTTP_201_CREATED,
                "counterpart": counterpart_serializer.data,
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
                "message": f"Error creating counterpart: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CounterpartDetailView(APIView):

    def get(self, request, id):
        try:
            data = Counterpart.objects.get(id=id)
            counterpart_serializer = CounterpartSerializer(data, many=False)
            response = {
                "message": "Counterpart retrieved successfully",
                "status": status.HTTP_200_OK,
                "counterpart": counterpart_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
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
