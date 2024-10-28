from .base import *
import os

DEBUG = False
ADMINS = [
('Eugenio Z', 'eugeniozangara_armada@outlook.com'),
]

ALLOWED_HOSTS = ['www.aquinus.com', 'aquinus.com', 'localhost', '127.0.0.1']
# DATABASES = {
#  'default': {
#     }
#  }


# ALLOWED_HOSTS = ['aquinus.com', 'www.aquinus.com']



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.getenv('DB_NAME_AQUINUS'),
#         'USER': os.getenv('DB_USER_AQUINUS'),
#         'PASSWORD': os.getenv('DB_PASSWORD_AQUINUS'),
#         'HOST': os.getenv('DB_HOST_AQUINUS', 'db'),
#         'PORT': os.getenv('DB_PORT_AQUINUS', '3306'),
#     },
#     "id8": {
#         "ENGINE": "django.db.backends.mysql",
#         'NAME': os.getenv('DB_NAME_ID8'),
#         'USER': os.getenv('DB_USER_ID8'),
#         'PASSWORD': os.getenv('DB_PASSWORD_ID8'),
#         'HOST': os.getenv('DB_HOST_ID8', 'db'),
#         'PORT': os.getenv('DB_PORT_ID8', '3306'),
#     },
# }

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": os.getenv('DB_NAME_AQUINUS', 'aquinus'),
#         "USER": os.getenv('DB_USER_AQUINUS', 'ezangara'),
#         "PASSWORD": os.getenv('DB_PASSWORD_AQUINUS', 'Armada2024@'),
#         "HOST": os.getenv('DB_HOST_AQUINUS', 'localhost'),
#         "PORT": os.getenv('DB_PORT_AQUINUS', '3306'),
#     },
#     "id8": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": os.getenv('DB_NAME_ID8', 'aspi'),
#         "USER": os.getenv('DB_USER_ID8', 'ezangara'),
#         "PASSWORD": os.getenv('DB_PASSWORD_ID8', 'Armada2024@'),
#         "HOST": os.getenv('DB_HOST_ID8', 'localhost'),
#         "PORT": os.getenv('DB_PORT_ID8', '3306'),
#     },
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv('DB_NAME_AQUINUS'),
        "USER": os.getenv('DB_USER_AQUINUS'),
        "PASSWORD": os.getenv('DB_PASSWORD_AQUINUS'),
        "HOST": os.getenv('DB_HOST_AQUINUS'),
        "PORT": os.getenv('DB_PORT_AQUINUS'),
    },
    "id8": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv('DB_NAME_ID8'),
        "USER": os.getenv('DB_USER_ID8'),
        "PASSWORD": os.getenv('DB_PASSWORD_ID8'),
        "HOST": os.getenv('DB_HOST_ID8'),
        "PORT": os.getenv('DB_PORT_ID8'),
    },
}


# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True