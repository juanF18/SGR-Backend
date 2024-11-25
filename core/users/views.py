from django.shortcuts import render
<<<<<<< HEAD
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserSerializer, UserValidator
from .models import User
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password


# Create your views here.
class UserView(APIView):
    def get(self, request):
        try:
            users = User.objects.all()
            user_serializer = UserSerializer(users, many=True)
            response = {
                "message": "Users retrieved successfully",
                "status": status.HTTP_200_OK,
                "users": user_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving users: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            user_validator = UserValidator(data)
            if not user_validator.is_valid():
                response = {
                    "message": "Invalid data",
                    "errors": user_validator.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create(
                name=data["name"],
                last_name=data["last_name"],
                email=data["email"],
                identification=data["identification"],
                password=make_password(data["password"]),
                role_id=data["role_id"],
                entity_id=data["entity_id"],
            )
            user_serializer = UserSerializer(user, many=False)
            response = {
                "message": "User created successfully",
                "status": status.HTTP_201_CREATED,
                "user": user_serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                "message": f"Error creating user: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetailView(APIView):

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            user_serializer = UserSerializer(user, many=False)
            response = {
                "message": "User retrieved successfully",
                "status": status.HTTP_200_OK,
                "user": user_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            response = {
                "message": "User not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error retrieving user: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginUserView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
=======

# Create your views here.
>>>>>>> develop
