# En un nuevo archivo, por ejemplo, exceptions.py
from django.core.exceptions import PermissionDenied

class CustomPermissionDenied(PermissionDenied):
    def __init__(self, message, redirect_url):
        self.redirect_url = redirect_url
        super().__init__(message)