# aquinus/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aquinus.settings.base')

app = Celery('aquinus')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre tareas automáticamente en cada aplicación instalada
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')



from celery.schedules import crontab

app = Celery('aquinus')

app.conf.beat_schedule = {
    'calcular-promedios-diarios': {
        'task': 'ruta_app.calcular_promedios_periodo',
        'schedule': crontab(hour=0, minute=0),  # Ejecuta todos los días a medianoche
    },
}