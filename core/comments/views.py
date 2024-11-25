from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentSerializer
from core.users.models import User


# Create your views here.
class CommentView(APIView):

    def post(self, request):
        try:
            data = request.data
            comment_text = data.get("comment_text")
            user = User.objects.get(id=data.get("user_id"))
            if not comment_text:
                response = {
                    "message": "comment_text is required",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            comment = Comment.objects.create(
                comment_text=comment_text,
                user_id=user,
            )
            comment.serializer = CommentSerializer(comment, many=False)
            response = {
                "message": "Comment created successfully",
                "status": status.HTTP_201_CREATED,
                "comment": comment.serializer.data,
            }

            return Response(response, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            response = {
                "message": "User not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error creating comment: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentDetailView(APIView):

    def get(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
            comment.serializer = CommentSerializer(comment, many=False)
            response = {
                "message": "Comment retrieved successfully",
                "status": status.HTTP_200_OK,
                "comment": comment.serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            response = {
                "message": "Comment not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error retrieving comment: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentUserView(APIView):

    def get(self, request, user_id):
        try:
            comments = Comment.objects.filter(user_id=user_id)
            comments.serializer = CommentSerializer(comments, many=True)
            response = {
                "message": "Comments retrieved successfully",
                "status": status.HTTP_200_OK,
                "comments": comments.serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            response = {
                "message": "Comments not found for this user",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error retrieving comments: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
