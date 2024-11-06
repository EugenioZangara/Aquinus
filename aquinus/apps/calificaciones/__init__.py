# apps/Calificaciones/__init__.py

# Importa celery para asegurar la detección automática de tareas
from aquinus.celery import app as celery_app

__all__ = ('celery_app',)

