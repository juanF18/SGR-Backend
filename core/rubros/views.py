from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Rubro
from rest_framework.views import APIView
from .serializers import RubroSerializer
from core.projects.models import Project


# Create your views here.
class RubroView(APIView):

    def get(self, request):
        try:
            data = Rubro.objects.all()
            rubro_serializer = RubroSerializer(data, many=True)
            response = {
                "message": "Rubros retrieved successfully",
                "status": status.HTTP_200_OK,
                "rubros": rubro_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving rubros: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            project = Project.objects.get(id=data["project_id"])
            rubro = Rubro.objects.create(
                descripcion=data["descripcion"],
                value_sgr=data["value_sgr"],
                project_id=project,
            )
            rubro_serializer = RubroSerializer(rubro, many=False)
            response = {
                "message": "Rubro created successfully",
                "status": status.HTTP_201_CREATED,
                "rubro": rubro_serializer.data,
            }

            return Response(response, status=status.HTTP_201_CREATED)
        except Project.DoesNotExist:
            response = {
                "message": "Project does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error creating rubro: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RubroDetailView(APIView):

    def get(self, request, pk):
        try:
            rubro = Rubro.objects.get(id=pk)
            response = {
                "message": "Rubro retrieved successfully",
                "status": status.HTTP_200_OK,
                "rubro": rubro,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Rubro.DoesNotExist:
            response = {
                "message": "Rubro does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error retrieving rubro: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
