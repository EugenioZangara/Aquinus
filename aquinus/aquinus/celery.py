from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aquinus.settings.local')

app = Celery('aquinus')

# Leer configuración desde Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubrir tareas automáticamente
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
