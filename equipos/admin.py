from django.contrib import admin
from django.utils.html import format_html

from .models import Equipo


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):

    list_display = (
        "escudo_admin",
        "nombre",
        "grupo",
    )

    list_display_links = (
        "nombre",
    )

    search_fields = (
        "nombre",
        "grupo",
    )

    list_filter = (
        "grupo",
    )

    ordering = (
        "grupo",
        "nombre",
    )

    list_per_page = 15

    def escudo_admin(self, obj):
        if obj.escudo:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:6px;object-fit:cover;">',
                obj.escudo.url
            )
        return "—"

    escudo_admin.short_description = "Escudo"
