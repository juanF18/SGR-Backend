from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Person
from rest_framework.views import APIView
from .serializers import PersonSerializer
from core.rubros.models import Rubro


# Create your views here.
class PersonView(APIView):
    def get(self, request):
        try:
            data = Person.objects.all()
            person_serializer = PersonSerializer(data, many=True)
            response = {
                "message": "Persons retrieved successfully",
                "status": status.HTTP_200_OK,
                "persons": person_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving persons: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            rubro = Rubro.objects.get(id=data["rubro_id"])
            person = Person.objects.create(
                job_title=data["job_title"],
                dedication=data["dedication"],
                weeks=data["weeks"],
                fees=data["fees"],
                value_hour=data["value_hour"],
                total=data["total"],
                rubro_id=rubro,
            )
            person_serializer = PersonSerializer(person, many=False)
            response = {
                "message": "Person created successfully",
                "status": status.HTTP_201_CREATED,
                "person": person_serializer.data,
            }

            return Response(response, status=status.HTTP_201_CREATED)
        except Rubro.DoesNotExist:
            response = {
                "message": "Rubro does not exist",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error creating person: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PersonDetailView(APIView):
    def get(self, request, id):
        try:
            person = Person.objects.get(id=id)
            person_serializer = PersonSerializer(person, many=False)
            response = {
                "message": "Person retrieved successfully",
                "status": status.HTTP_200_OK,
                "person": person_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            response = {
                "message": "Person does not exist",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error retrieving person: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
