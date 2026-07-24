from django.urls import path
from . import views


urlpatterns = [

    path(
        "estadisticas/",
        views.inicio_estadisticas,
        name="inicio_estadisticas"
    ),

    path(
        "tabla/",
        views.tabla_general,
        name="tabla_general"
    ),

    path(
        "goleadores/",
        views.tabla_goleadores,
        name="tabla_goleadores"
    ),

    path(
        "disciplina/",
        views.tabla_disciplinaria,
        name="tabla_disciplinaria"
    ),

]