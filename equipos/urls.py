from django.urls import path
from . import views

app_name = "equipos"

urlpatterns = [
    path("", views.lista_equipos, name="lista"),
    path("<int:equipo_id>/", views.detalle_equipo, name="detalle"),
]