from django.contrib import admin
from django.utils.html import format_html

from .models import Jornada, Partido


@admin.register(Jornada)
class JornadaAdmin(admin.ModelAdmin):

    list_display = (
        "numero",
        "cantidad_partidos",
    )

    search_fields = (
        "numero",
    )

    ordering = (
        "numero",
    )

    @admin.display(description="Partidos")
    def cantidad_partidos(self, obj):
        return obj.partidos.count()


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    readonly_fields = (
        "goles_local",
        "goles_visitante",
    )
    
    list_display = (
        "jornada",
        "partido_admin",
        "fecha",
        "hora",
        "cancha",
        "marcador_admin",
        "estado_admin",
    )

    list_display_links = (
        "partido_admin",
    )

    search_fields = (
        "equipo_local__nombre",
        "equipo_visitante__nombre",
        "cancha",
        "jornada__numero",
    )

    list_filter = (
        "jornada",
        "terminado",
        "fecha",
    )

    ordering = (
        "jornada__numero",
        "fecha",
        "hora",
    )

    list_select_related = (
        "jornada",
        "equipo_local",
        "equipo_visitante",
    )

    autocomplete_fields = (
        "jornada",
        "equipo_local",
        "equipo_visitante",
    )

    list_per_page = 20

    date_hierarchy = "fecha"

    fieldsets = (
        (
            "Encuentro",
            {
                "fields": (
                    "jornada",
                    "equipo_local",
                    "equipo_visitante",
                )
            }
        ),
        (
            "Programación",
            {
                "fields": (
                    "fecha",
                    "hora",
                    "cancha",
                )
            }
        ),
        (
            "Resultado",
            {
                "fields": (
                    "goles_local",
                    "goles_visitante",
                    "terminado",
                )
            }
        ),
    )

    actions = (
        "marcar_como_finalizados",
        "marcar_como_pendientes",
    )

    @admin.display(
        description="Partido",
        ordering="equipo_local__nombre"
    )
    def partido_admin(self, obj):
        return f"{obj.equipo_local} vs {obj.equipo_visitante}"

    @admin.display(description="Marcador")
    def marcador_admin(self, obj):
        return f"{obj.goles_local} - {obj.goles_visitante}"

    @admin.display(description="Estado")
    def estado_admin(self, obj):
        if obj.terminado:
            return format_html(
                """
                <span style="
                    color: #15803d;
                    background: #dcfce7;
                    padding: 5px 10px;
                    border-radius: 999px;
                    font-weight: 700;
                ">
                    Finalizado
                </span>
                """
            )

        return format_html(
            """
            <span style="
                color: #a16207;
                background: #fef9c3;
                padding: 5px 10px;
                border-radius: 999px;
                font-weight: 700;
            ">
                Pendiente
            </span>
            """
        )

    @admin.action(description="Marcar partidos como finalizados")
    def marcar_como_finalizados(self, request, queryset):
        cantidad = queryset.update(terminado=True)

        self.message_user(
            request,
            f"{cantidad} partido(s) fueron marcados como finalizados."
        )

    @admin.action(description="Marcar partidos como pendientes")
    def marcar_como_pendientes(self, request, queryset):
        cantidad = queryset.update(terminado=False)

        self.message_user(
            request,
            f"{cantidad} partido(s) fueron marcados como pendientes."
        )