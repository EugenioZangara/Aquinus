from .base import *


DEBUG = False
# ADMINS = [
# ('Eugenio Z', 'eugeniozangara_armada@outlook.com'),
# ]

ALLOWED_HOSTS = ['www.aquinus.com', 'aquinus.com', 'localhost', '127.0.0.1', '192.16.3.252']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "aquinus",
        "USER": "ezangara",
        "PASSWORD": "Armada2024@",
        "HOST": "192.16.0.252",  # O la dirección IP de tu servidor MySQL
        "PORT": "3306",  # El puerto de tu servidor MySQL},
    },
    "id8": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "aspi",
        "USER": "ezangara",
        "PASSWORD": "Armada2024@",
        "HOST": "192.16.0.252",  # O la dirección IP de tu servidor MySQL
        "PORT": "3306",  # El puerto de tu servidor MySQL},
    },
}


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": os.getenv('DB_NAME_AQUINUS'),
#         "USER": os.getenv('DB_USER_AQUINUS'),
#         "PASSWORD": os.getenv('DB_PASSWORD_AQUINUS'),
#         "HOST": os.getenv('DB_HOST_AQUINUS'),
#         "PORT": os.getenv('DB_PORT_AQUINUS'),
#     },
#     "id8": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": os.getenv('DB_NAME_ID8'),
#         "USER": os.getenv('DB_USER_ID8'),
#         "PASSWORD": os.getenv('DB_PASSWORD_ID8'),
#         "HOST": os.getenv('DB_HOST_ID8'),
#         "PORT": os.getenv('DB_PORT_ID8'),
#     },
# }


# Security
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True