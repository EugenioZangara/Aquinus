from .base import *
import environ
from pathlib import Path

DEBUG = True
ALLOWED_HOSTS = ['www.aquinus.com', 'aquinus.com', 'localhost', '127.0.0.1', '192.16.3.252']
"""
Configuración para trabajar en ESSA con servidor en linea

"""
env = environ.Env()
# Lee el archivo .env
env_path = env.str('ENV_PATH', '.env')
print(f"Leyendo variables de entorno desde: {env_path}")  # Debug
environ.Env.read_env(env.str('ENV_PATH', '.env'))

SECRET_KEY = env('DJANGO_SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DEFAULT_DB_NAME'),
        'USER': env('DEFAULT_DB_USER'),
        'PASSWORD': env('DEFAULT_DB_PASSWORD'),
        'HOST': env('DEFAULT_DB_HOST'),
        'PORT': env('DEFAULT_DB_PORT'),
    },
    'db2': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('ID8_DB_NAME'),
        'USER': env('ID8_DB_USER'),
        'PASSWORD': env('ID8_DB_PASSWORD'),
        'HOST': env('ID8_DB_HOST'),
        'PORT': env('ID8_DB_PORT'),
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
