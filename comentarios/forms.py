from django import forms
from .models import Comentario


class ComentarioForm(forms.ModelForm):

    class Meta:
        model = Comentario

        fields = [
            "nombre",
            "comentario",
        ]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Nombre, apodo o aka",
                    "maxlength": "80",
                }
            ),

            "comentario": forms.Textarea(
                attrs={
                    "placeholder": "Escribe tu comentario...",
                    "rows": 5,
                    "maxlength": "500",
                }
            ),
        }

        labels = {
            "nombre": "Nombre o apodo",
            "comentario": "Comentario",
        }