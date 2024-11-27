# Proyecto SGR

Este proyecto es una aplicación Django que expone una API REST utilizando Django REST Framework (DRF). La aplicación está diseñada para gestionar diferentes entidades, como **Usuarios**, **Proyectos**, **Roles**, **Rubros**, entre otros. Además, la documentación de la API está disponible a través de **Swagger**.

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Virtualenv (opcional, pero recomendado para gestionar entornos virtuales)

## Pasos para ejecutar el proyecto

### 1. Clonar el repositorio

Si aún no has clonado el repositorio, puedes hacerlo con el siguiente comando:

```bash
git clone https://github.com/juanF18/SGR-Backend
cd SGR-Backend
```

### 2. Crear un entorno virtual (opcional pero recomendado)

Es recomendable crear un entorno virtual para gestionar las dependencias de este proyecto de manera aislada. Si tienes `virtualenv` instalado, puedes crear y activar el entorno virtual de la siguiente manera:

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate
```

### 3. Instalar las dependencias

Una vez dentro del entorno virtual, instala las dependencias del proyecto usando `pip`:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` contiene todas las dependencias necesarias para ejecutar el proyecto, como Django, Django REST Framework, djangorestframework-simplejwt, drf-yasg para la documentación Swagger, entre otras.

### 4. Ejecutar las migraciones

Si es la primera vez que ejecutas el proyecto, debes aplicar las migraciones de la base de datos para crear las tablas necesarias.

```bash
python manage.py migrate
```

### 5. Crear un superusuario (opcional)

Si deseas acceder al panel de administración de Django (por ejemplo, para crear usuarios manualmente), puedes crear un superusuario:

```bash
python manage.py createsuperuser
```

Sigue las instrucciones en la terminal para ingresar el nombre de usuario, correo electrónico y contraseña.

### 6. Ejecutar el servidor de desarrollo

Ahora puedes ejecutar el servidor de desarrollo de Django para comenzar a trabajar con la API:

```bash
python manage.py runserver
```

Esto iniciará el servidor de desarrollo en `http://127.0.0.1:8000/`.

### 7. Acceder a la documentación Swagger

Una vez que el servidor esté en funcionamiento, puedes acceder a la documentación interactiva de la API a través de Swagger. Para hacerlo, simplemente abre tu navegador web y visita la siguiente URL:

```
http://127.0.0.1:8000/swagger/
```

Aquí podrás ver todos los endpoints de la API, realizar pruebas de las solicitudes y visualizar los detalles de cada uno de ellos.

### 8. Realizar peticiones a la API

La API está diseñada para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre las diferentes entidades. Puedes interactuar con estos endpoints utilizando herramientas como **Postman**, **Insomnia**, o directamente desde Swagger.

## Estructura del proyecto

La estructura básica del proyecto es la siguiente:

```
SGR-Backend/
│
├── core/                  # Contiene las aplicaciones principales (Usuarios, Proyectos, etc.)
│   ├── users/             # Gestión de usuarios
│   ├── roles/             # Roles de usuario
│   ├── rubros/            # Rubros relacionados con los proyectos
│   └── activities/        # Actividades relacionadas con los proyectos
│
├── sgr/           # Configuración principal de Django
│   ├── settings.py        # Configuración del proyecto
│   ├── urls.py            # Enlaces de URLs de la API
│   └── wsgi.py            # Archivo de entrada para el servidor WSGI
│
├── manage.py              # Script principal para administrar el proyecto Django
├── requirements.txt       # Lista de dependencias del proyecto
└── .env                   # Variables de entorno para la configuración (no se debe subir a GitHub)
```

## Endpoints disponibles

Una vez que el servidor esté en funcionamiento, puedes consultar los siguientes endpoints a través de la documentación Swagger:

- `GET /users/` - Obtener todos los usuarios.
- `POST /users/` - Crear un nuevo usuario.
- `GET /users/{id}/` - Obtener un usuario específico por ID.
- `POST /login/` - Iniciar sesión y obtener un token JWT.
- (y muchos más endpoints dependiendo de las entidades en tu proyecto).

## Consideraciones adicionales

- Asegúrate de que las dependencias estén instaladas correctamente y que el archivo `.env` esté configurado antes de ejecutar el proyecto.
- La documentación de la API se genera automáticamente utilizando **Swagger** y es accesible en `http://127.0.0.1:8000/swagger/`.
- Asegúrate de que la base de datos y otras configuraciones (como los servicios de correo) estén correctamente configuradas en el archivo `.env`.
