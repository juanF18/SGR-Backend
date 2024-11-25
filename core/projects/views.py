from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer, ProjectValidator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.entities.models import Entity


# Create your views here.
class ProjectView(APIView):

    def get(self, request):
        try:
            data = Project.objects.all()
            project_serializer = ProjectSerializer(data, many=True)
            response = {
                "message": "Projects retrieved successfully",
                "status": status.HTTP_200_OK,
                "projects": project_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving projects: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            entity = Entity.objects.get(id=data["entity_id"])
            project_validator = ProjectValidator(data)
            if not project_validator.is_valid():
                response = {
                    "message": "Invalid data for project creation validation",
                    "errors": project_validator.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            project = Project.objects.create(
                name=data["name"],
                description=data["description"],
                value=data["value"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                file_budget_url=data["file_budget_url"],
                file_activities_url=data["file_activities_url"],
                entity_id=entity,
            )
            project_serializer = ProjectSerializer(project, many=False)

            response = {
                "message": "Project created successfully",
                "status": status.HTTP_201_CREATED,
                "project": project_serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                "message": f"Error creating project: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectDetail(APIView):

    def get(self, request, id):
        try:
            project = self.get_object(id)
            project_serializer = ProjectSerializer(project, many=False)
            response = {
                "message": "Project retrieved successfully",
                "status": status.HTTP_200_OK,
                "project": project_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            response = {
                "message": "Project not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error retrieving project: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
