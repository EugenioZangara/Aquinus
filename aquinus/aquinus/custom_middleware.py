# middleware.py

from django.utils.deprecation import MiddlewareMixin

class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, 'current_user', request.user)
