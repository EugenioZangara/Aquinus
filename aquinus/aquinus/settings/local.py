from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
"""
Configuración para trabajar en ESSA con servidor en linea

"""
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "aquinus",
#         "USER": "ezangara",
#         "PASSWORD": "Armada2024@",
#         "HOST": "192.16.0.252",  # O la dirección IP de tu servidor MySQL
#         "PORT": "3306",  # El puerto de tu servidor MySQL},
#     },
#     "id8": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "aspi",
#         "USER": "ezangara",
#         "PASSWORD": "Armada2024@",
#         "HOST": "192.16.0.252",  # O la dirección IP de tu servidor MySQL
#         "PORT": "3306",  # El puerto de tu servidor MySQL},
#     },
# }
"""
Configuración para trabajar OFFLINE
"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "aquinus",
        "USER": "ezangara",
        "PASSWORD": "Armada2024@",
        "HOST": "localhost",  # O la dirección IP de tu servidor MySQL
        "PORT": "3306",  # El puerto de tu servidor MySQL},
    },
    "id8": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "aspi",
        "USER": "ezangara",
        "PASSWORD": "Armada2024@",
        "HOST": "localhost",  # O la dirección IP de tu servidor MySQL
        "PORT": "3306",  # El puerto de tu servidor MySQL},
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
# URL para acceder a archivos estáticos
STATIC_URL = '/static/'

# Directorio donde se recolectan los archivos estáticos para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Directorios adicionales donde Django buscará archivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Aquí puedes colocar archivos estáticos globales para tu proyecto
]

# # Configuración para pruebas de Celery en modo "eager"
# CELERY_TASK_ALWAYS_EAGER = True
# CELERY_TASK_EAGER_PROPAGATES = True  # Esto permitirá que veas cualquier excepción lanzada
# Configuración de Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # O tu broker preferido
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'  # O tu zona horaria
