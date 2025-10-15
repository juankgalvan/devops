from django.urls import path
from . import views

urlpatterns = [
    path('insertar', views.insertar_usuario),
    path('usuarios', views.listar_usuarios),
    path('buscar/<int:codigo>', views.buscar_usuario),
    path('modificar', views.modificar_usuario),
    path('eliminar/<int:codigo>', views.eliminar_usuario),
]
