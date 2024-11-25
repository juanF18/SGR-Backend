from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer
from core.rubros.models import Rubro


# Create your views here.
class ItemView(APIView):

    def get(self, request):
        try:
            items = Item.objects.all()
            item_serializer = ItemSerializer(items, many=True)
            response = {
                "message": "Items retrieved successfully",
                "status": status.HTTP_200_OK,
                "items": item_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error retrieving items: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            rubro = Rubro.objects.get(id=data["rubro_id"])
            item = Item.objects.create(
                description=data["description"],
                justificacion=data["justificacion"],
                quantity=data["quantity"],
                unit_value=data["unit_value"],
                total_value=data["total_value"],
                rubro_id=rubro,
            )
            item_serializer = ItemSerializer(item)
            response = {
                "message": "Item created successfully",
                "status": status.HTTP_201_CREATED,
                "item": item_serializer.data,
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
                "message": f"Error creating item: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ItemDetailView(APIView):

    def get(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            item_serializer = ItemSerializer(item)
            response = {
                "message": "Item retrieved successfully",
                "status": status.HTTP_200_OK,
                "item": item_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            response = {
                "message": "Item does not exist",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": f"Error retrieving item: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
