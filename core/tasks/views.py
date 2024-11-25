from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Task
from rest_framework.views import APIView
from .serializers import TaskSerializer
from core.activities.models import Activity


# Create your views here.
class TaskView(APIView):
    def get(self, request):
        try:
            data = Task.objects.all()
            task_serializer = TaskSerializer(data, many=True)
            response = {
                "message": "Tasks retrieved successfully",
                "status": status.HTTP_200_OK,
                "tasks": task_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving tasks: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            activity = Activity.objects.get(id=data["activity_id"])
            task = Task.objects.create(
                name=data["name"],
                description=data["description"],
                state=data["state"],
                activity_id=activity,
            )
            task_serializer = TaskSerializer(task, many=False)
            response = {
                "message": "Task created successfully",
                "status": status.HTTP_201_CREATED,
                "task": task_serializer.data,
            }

            return Response(response, status=status.HTTP_201_CREATED)
        except Activity.DoesNotExist:
            response = {
                "message": "Activity does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error creating task: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskDetailView(APIView):
    def get(self, request, id):
        try:
            task = Task.objects.get(id=id)
            task_serializer = TaskSerializer(task, many=False)
            response = {
                "message": "Task retrieved successfully",
                "status": status.HTTP_200_OK,
                "task": task_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            response = {
                "message": "Task does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error retrieving task: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
