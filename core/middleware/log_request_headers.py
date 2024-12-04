from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import TokenError


class LogRequestHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log de los headers de la solicitud
        print("Headers de la solicitud:")
        for key, value in request.headers.items():
            print(f"{key}: {value}")

        # Si hay un Authorization header, decodificar el token
        auth_header = request.headers.get("Authorization", None)
        if auth_header:
            try:
                # Extraemos el token Bearer
                token = auth_header.split(" ")[1]  # `Bearer <token>`

                # Decodificamos el token
                try:
                    untoken = UntypedToken(token)
                    print(f"Token decodificado: {untoken.payload}")
                    user_id = untoken.payload.get("id")
                    print(f"UUID del usuario: {user_id}")  # Este es tu UUID
                except TokenError as e:
                    print(f"Error al decodificar el token: {str(e)}")
            except IndexError:
                print("El header 'Authorization' no tiene un token válido")

        # Continuamos con la solicitud
        response = self.get_response(request)
        return response
