"""
WSGI config for aquinus project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Añade la ruta del proyecto al path de Python
path = '/ruta/a/tu/proyecto/aquinus'
if path not in sys.path:
    sys.path.append(path)
    
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aquinus.settings.prod')

application = get_wsgi_application()
