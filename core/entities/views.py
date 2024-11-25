from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Entity
from .serializers import EntitySerializer, EntityValidator


# Create your views here.
class EntityView(APIView):
    def get(self, request):
        try:
            entities = Entity.objects.all()
            entity_serializer = EntitySerializer(entities, many=True)
            response = {
                "message": "Entities retrieved successfully",
                "status": status.HTTP_200_OK,
                "entities": entity_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving entities: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            entity_validator = EntityValidator(data)
            if not entity_validator.is_valid():
                response = {
                    "message": "Invalid data",
                    "errors": entity_validator.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            entity = Entity.objects.create(
                name=data["name"],
                description=data["description"],
                address=data["address"],
                phone=data["phone"],
                email=data["email"],
            )
            entity_serializer = EntitySerializer(entity, many=False)
            response = {
                "message": "Entity created successfully",
                "status": status.HTTP_201_CREATED,
                "entity": entity_serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                "message": f"Error creating entity: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            entity = Entity.objects.get(id=id)
            data = request.data
            entity.name = data["name"]
            entity.email = data["email"]
            entity.phone = data["phone"]
            entity.address = data["address"]
            entity.city = data["city"]
            entity.save()
            entity_serializer = EntitySerializer(entity, many=False)
            response = {
                "message": "Entity updated successfully",
                "status": status.HTTP_200_OK,
                "entity": entity_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Entity.DoesNotExist:
            response = {
                "message": "Entity not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error updating entity: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EntityDetailView(APIView):

    def get(self, request, id):
        try:
            entity = Entity.objects.get(id=id)
            entity_serializer = EntitySerializer(entity, many=False)
            response = {
                "message": "Entity retrieved successfully",
                "status": status.HTTP_200_OK,
                "entity": entity_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Entity.DoesNotExist:
            response = {
                "message": "Entity not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error retrieving entity: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
