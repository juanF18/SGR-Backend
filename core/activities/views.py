from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Activity
from rest_framework.views import APIView
from .serializers import ActivitySerializer
from core.projects.models import Project
from core.rubros.models import Rubro


# Create your views here.
class ActivityView(APIView):

    def get(self, request):
        try:
            data = Activity.objects.all()
            activity_serializer = ActivitySerializer(data, many=True)
            response = {
                "message": "Activities retrieved successfully",
                "status": status.HTTP_200_OK,
                "activities": activity_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving activities: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            project = Project.objects.get(id=data["project_id"])
            rubro = Rubro.objects.get(id=data["rubro_id"])
            activity = Activity.objects.create(
                name=data["name"],
                description=data["description"],
                type=data["type"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                state=data["state"],
                project_id=project,
                rubro_id=rubro,
            )
            activity_serializer = ActivitySerializer(activity, many=False)
            response = {
                "message": "Activity created successfully",
                "status": status.HTTP_201_CREATED,
                "activity": activity_serializer.data,
            }

            return Response(response, status=status.HTTP_201_CREATED)
        except Project.DoesNotExist:
            response = {
                "message": "Project does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Rubro.DoesNotExist:
            response = {
                "message": "Rubro does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error creating activity: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ActivityDetailView(APIView):

    def get(self, request, pk):
        try:
            activity = Activity.objects.get(id=pk)
            response = {
                "message": "Activity retrieved successfully",
                "status": status.HTTP_200_OK,
                "activity": activity,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Activity.DoesNotExist:
            response = {
                "message": "Activity does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error retrieving activity: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
