from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Role
from .serializers import RoleSerializer, RoleValidator


# Create your views here.
class RoleView(APIView):

    def get(self, request):
        try:
            data = Role.objects.all()
            role_serializer = RoleSerializer(data, many=True)
            response = {
                "message": "Roles retrieved successfully",
                "status": status.HTTP_200_OK,
                "roles": role_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving roles: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            role_validator = RoleValidator(data)
            if not role_validator.is_valid():
                response = {
                    "message": "Invalid data for role creation validation",
                    "errors": role_validator.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            role = Role.objects.create(
                name=data["name"],
            )
            role_serializer = RoleSerializer(role, many=False)

            response = {
                "message": "Role created successfully",
                "status": status.HTTP_201_CREATED,
                "role": role_serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                "message": f"Error creating role: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            data = request.data
            role = self.get_object(id)
            role_validator = RoleValidator(data)
            if not role_validator.is_valid():
                response = {
                    "message": "Invalid data",
                    "errors": role_validator.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            role.name = data["name"]
            role.save()
            role_serializer = RoleSerializer(role, many=False)
            response = {
                "message": "Role updated successfully",
                "status": status.HTTP_200_OK,
                "role": role_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error updating role: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RoleDetailView(APIView):

    def get(self, request, id):
        try:
            role = Role.objects.get(id=id)
            role_serializer = RoleSerializer(role, many=False)
            response = {
                "message": "Role retrieved successfully",
                "status": status.HTTP_200_OK,
                "role": role_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            response = {
                "message": "Role not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
