# myapp/urls.py
from django.urls import path
from .views import CustomLoginView, UsuarioPerfilCreateView
from django.contrib.auth import views as auth_views

app_name='usuarios'
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
         path('create_user/', UsuarioPerfilCreateView.as_view(), name='create_user'),

]
