from django import forms
from django.contrib import admin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import path
from django.utils.html import format_html

from info.models import Partido
from jugadores.models import Jugador

from .models import Gol, Tarjeta


# =====================================================
# FORMULARIO DE GOLES
# =====================================================

class GolAdminForm(forms.ModelForm):

    class Meta:
        model = Gol
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["jugador"].queryset = Jugador.objects.none()

        partido_id = None

        # Cuando se envía el formulario
        if "partido" in self.data:
            try:
                partido_id = int(self.data.get("partido"))
            except (TypeError, ValueError):
                partido_id = None

        # Cuando se edita un gol existente
        elif self.instance.pk:
            partido_id = self.instance.partido_id

        if partido_id:
            try:
                partido = Partido.objects.get(pk=partido_id)

                self.fields["jugador"].queryset = (
                    Jugador.objects
                    .filter(
                        Q(equipo_id=partido.equipo_local_id)
                        | Q(equipo_id=partido.equipo_visitante_id)
                    )
                    .select_related("equipo")
                    .order_by(
                        "equipo__nombre",
                        "numero",
                        "nombre",
                    )
                )

            except Partido.DoesNotExist:
                pass


# =====================================================
# FORMULARIO DE TARJETAS
# =====================================================

class TarjetaAdminForm(forms.ModelForm):

    class Meta:
        model = Tarjeta
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["jugador"].queryset = Jugador.objects.none()

        partido_id = None

        if "partido" in self.data:
            try:
                partido_id = int(self.data.get("partido"))
            except (TypeError, ValueError):
                partido_id = None

        elif self.instance.pk:
            partido_id = self.instance.partido_id

        if partido_id:
            try:
                partido = Partido.objects.get(pk=partido_id)

                self.fields["jugador"].queryset = (
                    Jugador.objects
                    .filter(
                        Q(equipo_id=partido.equipo_local_id)
                        | Q(equipo_id=partido.equipo_visitante_id)
                    )
                    .select_related("equipo")
                    .order_by(
                        "equipo__nombre",
                        "numero",
                        "nombre",
                    )
                )

            except Partido.DoesNotExist:
                pass


# =====================================================
# ADMINISTRACIÓN DE GOLES
# =====================================================

@admin.register(Gol)
class GolAdmin(admin.ModelAdmin):

    form = GolAdminForm

    list_display = (
        "jugador",
        "equipo_admin",
        "partido",
        "minuto_admin",
    )

    search_fields = (
        "jugador__nombre",
        "jugador__apellidos",
        "jugador__equipo__nombre",
        "partido__equipo_local__nombre",
        "partido__equipo_visitante__nombre",
    )

    list_filter = (
        "jugador__equipo",
        "partido__jornada",
    )

    list_select_related = (
        "jugador",
        "jugador__equipo",
        "partido",
        "partido__equipo_local",
        "partido__equipo_visitante",
    )

    autocomplete_fields = (
        "partido",
    )

    ordering = (
        "-partido__fecha",
        "minuto",
    )

    list_per_page = 25

    # Carga el JavaScript en el formulario del admin
    class Media:
        js = (
            "estadisticas/js/jugadores_por_partido.js",
        )

    # Ruta personalizada del administrador
    def get_urls(self):
        urls = super().get_urls()

        urls_personalizadas = [
            path(
                "jugadores-por-partido/",
                self.admin_site.admin_view(
                    self.jugadores_por_partido
                ),
                name="estadisticas_gol_jugadores_por_partido",
            ),
        ]

        return urls_personalizadas + urls

    # Devuelve los jugadores del partido en formato JSON
    def jugadores_por_partido(self, request):
        partido_id = request.GET.get("partido_id")

        if not partido_id:
            return JsonResponse({
                "jugadores": []
            })

        try:
            partido = Partido.objects.get(pk=partido_id)

        except Partido.DoesNotExist:
            return JsonResponse({
                "jugadores": []
            })

        jugadores = (
            Jugador.objects
            .filter(
                equipo_id__in=[
                    partido.equipo_local_id,
                    partido.equipo_visitante_id,
                ]
            )
            .select_related("equipo")
            .order_by(
                "equipo__nombre",
                "numero",
                "nombre",
            )
        )

        datos = [
            {
                "id": jugador.pk,
                "texto": (
                    f"{jugador.equipo.nombre} — "
                    f"#{jugador.numero} "
                    f"{jugador.nombre} {jugador.apellidos}"
                ),
            }
            for jugador in jugadores
        ]

        return JsonResponse({
            "jugadores": datos
        })

    @admin.display(
        description="Equipo",
        ordering="jugador__equipo__nombre"
    )
    def equipo_admin(self, obj):
        return obj.jugador.equipo

    @admin.display(
        description="Minuto",
        ordering="minuto"
    )
    def minuto_admin(self, obj):
        if obj.minuto is not None:
            return f"{obj.minuto}'"

        return "—"


# =====================================================
# ADMINISTRACIÓN DE TARJETAS
# =====================================================

@admin.register(Tarjeta)
class TarjetaAdmin(admin.ModelAdmin):

    form = TarjetaAdminForm

    list_display = (
        "jugador",
        "equipo_admin",
        "partido",
        "tipo_admin",
    )

    search_fields = (
        "jugador__nombre",
        "jugador__apellidos",
        "jugador__equipo__nombre",
        "partido__equipo_local__nombre",
        "partido__equipo_visitante__nombre",
    )

    list_filter = (
        "tipo",
        "jugador__equipo",
        "partido__jornada",
    )

    list_select_related = (
        "jugador",
        "jugador__equipo",
        "partido",
        "partido__equipo_local",
        "partido__equipo_visitante",
    )

    autocomplete_fields = (
        "partido",
    )

    ordering = (
        "-partido__fecha",
        "tipo",
    )

    list_per_page = 25

    @admin.display(
        description="Equipo",
        ordering="jugador__equipo__nombre"
    )
    def equipo_admin(self, obj):
        return obj.jugador.equipo

    @admin.display(
        description="Tarjeta",
        ordering="tipo"
    )
    def tipo_admin(self, obj):

        if obj.tipo == "ROJA":
            return format_html(
                """
                <span style="
                    color: white;
                    background: #dc2626;
                    padding: 5px 10px;
                    border-radius: 6px;
                    font-weight: 700;
                ">
                    Roja
                </span>
                """
            )

        return format_html(
            """
            <span style="
                color: #111;
                background: #facc15;
                padding: 5px 10px;
                border-radius: 6px;
                font-weight: 700;
            ">
                Amarilla
            </span>
            """
        )
    
    
    class Media:
        js = (
            "estadisticas/js/jugadores_por_partido.js",
        )

    def get_urls(self):
        urls = super().get_urls()

        urls_personalizadas = [
            path(
                "jugadores-por-partido/",
                self.admin_site.admin_view(
                    self.jugadores_por_partido
                ),
                name="estadisticas_tarjeta_jugadores_por_partido",
            ),
        ]

        return urls_personalizadas + urls
    
    def jugadores_por_partido(self, request):
        partido_id = request.GET.get("partido_id")

        if not partido_id:
            return JsonResponse({
                "jugadores": []
            })

        try:
            partido = Partido.objects.get(
                pk=partido_id
            )
        except Partido.DoesNotExist:
            return JsonResponse({
                "jugadores": []
            })

        jugadores = (
            Jugador.objects
            .filter(
                equipo_id__in=[
                    partido.equipo_local_id,
                    partido.equipo_visitante_id,
                ]
            )
            .select_related("equipo")
            .order_by(
                "equipo__nombre",
                "numero",
                "nombre",
            )
        )

        datos = [
            {
                "id": jugador.pk,
                "texto": (
                    f"{jugador.equipo.nombre} — "
                    f"#{jugador.numero} "
                    f"{jugador.nombre} "
                    f"{jugador.apellidos}"
                ),
            }
            for jugador in jugadores
        ]

        return JsonResponse({
            "jugadores": datos
        })