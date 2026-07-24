from django.contrib import admin
from .models import Comentario


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "resumen_comentario",
        "fecha",
    )

    search_fields = (
        "nombre",
        "comentario",
    )

    ordering = (
        "-fecha",
    )

    readonly_fields = (
        "fecha",
    )

    def resumen_comentario(self, obj):
        if len(obj.comentario) > 60:
            return f"{obj.comentario[:60]}..."

        return obj.comentario

    resumen_comentario.short_description = "Comentario"