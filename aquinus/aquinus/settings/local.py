from .base import *

DEBUG = True

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
