from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ComentarioForm
from .models import Comentario


def lista_comentarios(request):

    comentarios = Comentario.objects.all()

    if request.method == "POST":

        formulario = ComentarioForm(request.POST)

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                "Tu comentario fue publicado correctamente."
            )

            return redirect("comentarios:lista")

    else:
        formulario = ComentarioForm()

    return render(
        request,
        "comentarios/lista_comentarios.html",
        {
            "comentarios": comentarios,
            "formulario": formulario,
        }
    )