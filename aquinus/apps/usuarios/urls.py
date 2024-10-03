# myapp/urls.py
from django.urls import path
from .views import CustomLoginView, UsuarioPerfilCreateView, UserListView, DeleteUser,UserUpdateView, CambiarContrasenaView, ProfesoresListView, ProfesorDetailView, ResetearContrasenaView
from django.contrib.auth import views as auth_views
from .views_htmx import get_usuarios_x_dni

app_name='usuarios'
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
         path('create_user/', UsuarioPerfilCreateView.as_view(), name='create_user'),
         path('ver_usuarios/', UserListView.as_view(), name='ver_usuarios'),
             path('usuarios/eliminar/<int:pk>/', DeleteUser.as_view(), name='eliminar_usuario'),
    path('modificar_usuario/<int:pk>/', UserUpdateView.as_view(), name='modificar_usuario'),
    path('cambiar_contrasena/', CambiarContrasenaView.as_view(), name='cambiar_contrasena'),
    path('consultar_profesores/', ProfesoresListView.as_view(), name='consultar_profesores'),
    path('ver_detalles_profesor/<int:pk>/', ProfesorDetailView.as_view(), name="ver_detalles_profesor"),
    path('resetear_contrasenia/', ResetearContrasenaView.as_view(), name='resetear_contrasenia'),
    path('resetear_contrasenia/<int:pk>/', ResetearContrasenaView.as_view(), name='resetear_contrasenia'),
    path('get_usuarios_x_dni/',get_usuarios_x_dni,name='get_usuarios_x_dni')


]
