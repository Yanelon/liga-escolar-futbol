from django.contrib import admin
from django.utils.html import format_html

from .models import Jugador


@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):

    list_display = (
        "foto_admin",
        "nombre_completo",
        "equipo",
        "numero",
        "posicion",
        "edad",
    )

    list_display_links = (
        "foto_admin",
        "nombre_completo",
    )

    search_fields = (
        "nombre",
        "apellidos",
        "equipo__nombre",
        "numero",
    )

    list_filter = (
        "equipo",
        "posicion",
    )

    ordering = (
        "equipo__nombre",
        "numero",
    )

    list_select_related = (
        "equipo",
    )

    list_per_page = 20

    autocomplete_fields = (
        "equipo",
    )

    readonly_fields = (
        "vista_previa_foto",
    )

    fieldsets = (
        (
            "Información personal",
            {
                "fields": (
                    "nombre",
                    "apellidos",
                    "edad",
                )
            }
        ),
        (
            "Información deportiva",
            {
                "fields": (
                    "equipo",
                    "numero",
                    "posicion",
                )
            }
        ),
        (
            "Fotografía",
            {
                "fields": (
                    "foto",
                    "vista_previa_foto",
                )
            }
        ),
    )

    @admin.display(description="Foto")
    def foto_admin(self, obj):
        if obj.foto:
            return format_html(
                """
                <img
                    src="{}"
                    width="45"
                    height="45"
                    style="
                        object-fit: cover;
                        border-radius: 50%;
                        border: 2px solid #22c55e;
                    "
                >
                """,
                obj.foto.url
            )

        return format_html(
            """
            <div style="
                width: 45px;
                height: 45px;
                border-radius: 50%;
                background: #333;
                color: #fff;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
            ">
                {}
            </div>
            """,
            obj.nombre[0].upper() if obj.nombre else "?"
        )

    @admin.display(
        description="Jugador",
        ordering="apellidos"
    )
    def nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellidos}"

    @admin.display(description="Vista previa")
    def vista_previa_foto(self, obj):
        if not obj.pk:
            return "Guarda primero al jugador para ver la fotografía."

        if obj.foto:
            return format_html(
                """
                <img
                    src="{}"
                    width="160"
                    height="160"
                    style="
                        object-fit: cover;
                        border-radius: 12px;
                        border: 3px solid #22c55e;
                    "
                >
                """,
                obj.foto.url
            )

        return "Este jugador no tiene fotografía."
