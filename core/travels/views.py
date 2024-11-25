from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Travel
from rest_framework.views import APIView
from .serializers import TravelSerializer
from core.rubros.models import Rubro


# Create your views here.
class TravelView(APIView):

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
