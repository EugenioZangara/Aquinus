# myapp/urls.py
from django.urls import path
from .views import CustomLoginView, UsuarioPerfilCreateView, UserListView, DeleteUser,UserUpdateView, CambiarContrasenaView
from django.contrib.auth import views as auth_views

app_name='usuarios'
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
         path('create_user/', UsuarioPerfilCreateView.as_view(), name='create_user'),
         path('ver_usuarios/', UserListView.as_view(), name='ver_usuarios'),
             path('usuarios/eliminar/<int:pk>/', DeleteUser.as_view(), name='eliminar_usuario'),
    path('modificar_usuario/<int:pk>/', UserUpdateView.as_view(), name='modificar_usuario'),
    path('cambiar_contrasena/', CambiarContrasenaView.as_view(), name='cambiar_contrasena'),


]
