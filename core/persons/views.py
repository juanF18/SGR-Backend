from rest_framework import status
from rest_framework.response import Response
from .models import Person
from rest_framework.views import APIView
from .serializers import PersonSerializer
from core.rubros.models import Rubro
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Definir el cuerpo de la solicitud para el POST en PersonView
person_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "job_title": openapi.Schema(
            type=openapi.TYPE_STRING, description="Título del trabajo de la persona"
        ),
        "dedication": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Dedicación de la persona (Tiempo completo, medio tiempo, etc.)",
        ),
        "weeks": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Número de semanas trabajadas"
        ),
        "fees": openapi.Schema(
            type=openapi.TYPE_NUMBER,
            format=openapi.FORMAT_FLOAT,
            description="Honorarios",
        ),
        "value_hour": openapi.Schema(
            type=openapi.TYPE_NUMBER,
            format=openapi.FORMAT_FLOAT,
            description="Valor por hora de trabajo",
        ),
        "total": openapi.Schema(
            type=openapi.TYPE_NUMBER,
            format=openapi.FORMAT_FLOAT,
            description="Total por el trabajo realizado",
        ),
        "rubro_id": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="ID del rubro relacionado con la persona",
        ),
    },
)


class PersonView(APIView):
    """
    Class to handle HTTP requests related to persons

    @methods:
    - get: Get all persons
    - post: Create a new person
    """

    # Documentar el método GET para obtener todas las personas
    @swagger_auto_schema(
        operation_description="Obtener todas las personas",
        responses={
            200: openapi.Response(
                description="Personas recuperadas correctamente",
                schema=PersonSerializer(many=True),
            ),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request):
        """
        Get all persons
        @param request: HTTP request
        @return: JSON response
        """

        try:
            data = Person.objects.all()
            person_serializer = PersonSerializer(data, many=True)

            return Response(person_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": f"Error obteniendo las personas: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Documentar el método POST para crear una nueva persona
    @swagger_auto_schema(
        operation_description="Crear una nueva persona",
        request_body=person_request_body,
        responses={
            201: openapi.Response(
                description="Persona creada correctamente", schema=PersonSerializer
            ),
            404: openapi.Response(description="Rubro no encontrado"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def post(self, request):
        """
        Create a new person
        @param request: HTTP request
        @return: JSON response
        """

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

            return Response(person_serializer.data, status=status.HTTP_201_CREATED)
        except Rubro.DoesNotExist:
            response = {
                "message": "Rubro no encontrado",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error creando la persona: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PersonDetailView(APIView):
    """
    Class to handle HTTP requests related to a specific person

    @methods:
    - get: Get a specific person by ID
    - put: Update a specific person by ID
    - delete: Delete a specific person by ID
    """

    # Documentar el método GET para obtener una persona específica por ID
    @swagger_auto_schema(
        operation_description="Obtener una persona específica por ID",
        responses={
            200: openapi.Response(
                description="Persona recuperada correctamente", schema=PersonSerializer
            ),
            404: openapi.Response(description="Persona no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def get(self, request, id):
        """
        Get a specific person by ID
        @param request: HTTP request
        @param id: Person ID
        @return: JSON response
        """

        try:
            person = Person.objects.get(id=id)
            person_serializer = PersonSerializer(person, many=False)

            return Response(person_serializer.data, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            response = {
                "message": "Persona no encontrada",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error obteniendo la persona: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Actualizar una persona específica por ID",
        request_body=person_request_body,
        responses={
            200: openapi.Response(
                description="Persona actualizada correctamente", schema=PersonSerializer
            ),
            404: openapi.Response(description="Persona no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def put(self, request, pk):
        """
        Update a specific person by ID
        @param request: HTTP request
        @param id: Person ID
        @return: JSON response
        """

        try:
            person = Person.objects.get(id=pk)

            data = request.data

            if data.get("rubro_id"):
                rubro = Rubro.objects.get(id=data["rubro_id"])
                person.rubro_id = rubro

            person.job_title = data.get("job_title", person.job_title)
            person.dedication = data.get("dedication", person.dedication)
            person.weeks = data.get("weeks", person.weeks)
            person.fees = data.get("fees", person.fees)
            person.value_hour = data.get("value_hour", person.value_hour)
            person.total = data.get("total", person.total)

            person.save()

            person_serializer = PersonSerializer(person, many=False)

            return Response(person_serializer.data, status=status.HTTP_200_OK)
        except Rubro.DoesNotExist:
            response = {
                "message": "Rubro no encontrado",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Person.DoesNotExist:
            response = {
                "message": "Persona no encontrada",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error actualizando la persona: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Eliminar una persona específica por ID",
        responses={
            204: openapi.Response(description="Persona eliminada correctamente"),
            404: openapi.Response(description="Persona no encontrada"),
            500: openapi.Response(description="Error interno del servidor"),
        },
    )
    def delete(self, request, pk):
        """
        Delete a specific person by ID
        @param request: HTTP request
        @param id: Person ID
        @return: JSON response
        """

        try:
            person = Person.objects.get(id=pk)
            person.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Person.DoesNotExist:
            response = {
                "message": "Persona no encontrada",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "message": f"Error eliminando la persona: {str(e)}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
