from .base import *
import os

DEBUG = False
ADMINS = [
('Eugenio Z', 'eugeniozangara_armada@outlook.com'),
]
ALLOWED_HOSTS = ['aquinus.com', 'www.aquinus.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME_AQUINUS'),
        'USER': os.getenv('DB_USER_AQUINUS'),
        'PASSWORD': os.getenv('DB_PASSWORD_AQUINUS'),
        'HOST': os.getenv('DB_HOST_AQUINUS', 'db'),
        'PORT': os.getenv('DB_PORT_AQUINUS', '3306'),
    },
    "id8": {
        "ENGINE": "django.db.backends.mysql",
        'NAME': os.getenv('DB_NAME_ID8'),
        'USER': os.getenv('DB_USER_ID8'),
        'PASSWORD': os.getenv('DB_PASSWORD_ID8'),
        'HOST': os.getenv('DB_HOST_ID8', 'db'),
        'PORT': os.getenv('DB_PORT_ID8', '3306'),
    },
}



