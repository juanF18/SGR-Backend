from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentSerializer
from core.users.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Definir el cuerpo de la solicitud para el POST en CommentView
comment_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "comment_text": openapi.Schema(
            type=openapi.TYPE_STRING, description="Texto del comentario"
        ),
        "user_id": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="ID del usuario que realiza el comentario",
        ),
    },
)


class CommentView(APIView):

    """
    Class to handle HTTP requests related to comments

    @methods:
    - get: Get all comments
    - post: Create a new comment
    """

    # Documentar el método POST para crear un nuevo comentario
    @swagger_auto_schema(
        operation_description="Crear un nuevo comentario",
        request_body=comment_request_body,
        responses={
            201: openapi.Response(
                description="Comentario creado correctamente", schema=CommentSerializer
            ),
            400: openapi.Response(description="El campo 'comment_text' es requerido"),
            404: openapi.Response(description="Usuario no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):

        """
        Create a new comment
        @param request: HTTP request
        @return: HTTP response
        """

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

            return Response(comment.serializer.data, status=status.HTTP_201_CREATED)
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

    """
    Class to handle HTTP requests related to a specific comment

    @methods:
    - get: Get comment details
    """
    
    # Documentar el método GET para obtener los detalles de un comentario
    @swagger_auto_schema(
        operation_description="Obtener los detalles de un comentario",
        responses={
            200: openapi.Response(
                description="Comentario recuperado correctamente",
                schema=CommentSerializer,
            ),
            404: openapi.Response(description="Comentario no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, pk):

        """
        Get a specific comment by ID
        @param request: HTTP request
        @param pk: Comment ID
        @return: JSON response
        """

        try:
            comment = Comment.objects.get(id=pk)
            comment.serializer = CommentSerializer(comment, many=False)

            return Response(comment.serializer.data, status=status.HTTP_200_OK)
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

    """
    Class to handle HTTP requests related to comments by user

    @methods:
    - get: Get all comments by user
    """

    # Documentar el método GET para obtener todos los comentarios de un usuario
    @swagger_auto_schema(
        operation_description="Obtener todos los comentarios de un usuario",
        responses={
            200: openapi.Response(
                description="Comentarios recuperados correctamente",
                schema=CommentSerializer(many=True),
            ),
            404: openapi.Response(
                description="Comentarios no encontrados para este usuario"
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, user_id):

        """
        Get all comments by user
        @param request: HTTP request
        @param user_id: User ID
        @return: JSON response
        """
        
        try:
            comments = Comment.objects.filter(user_id=user_id)
            comments.serializer = CommentSerializer(comments, many=True)

            return Response(comments.serializer.data, status=status.HTTP_200_OK)
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
