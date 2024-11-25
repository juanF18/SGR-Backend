from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Cdps
from rest_framework.views import APIView
from .serializers import CdpsSerializer
from core.rubros.models import Rubro


# Create your views here.
class CdpsView(APIView):
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
