from django.urls import path
from . import views

app_name = "jugadores"

urlpatterns = [
    path(
        "<int:jugador_id>/",
        views.detalle_jugador,
        name="detalle"
    ),
]