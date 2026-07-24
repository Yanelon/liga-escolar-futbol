document.addEventListener("DOMContentLoaded", function () {
    const partidoSelect = document.getElementById("id_partido");
    const jugadorSelect = document.getElementById("id_jugador");

    if (!partidoSelect || !jugadorSelect) {
        console.error("No se encontraron los campos partido o jugador.");
        return;
    }

    let cargando = false;
    let ultimoPartidoCargado = null;
    let jugadorActual = jugadorSelect.value;

    async function cargarJugadores() {
        const partidoId = partidoSelect.value;

        /*
        Select2 puede disparar dos eventos casi al mismo tiempo.
        Si ya estamos cargando ese mismo partido, ignoramos
        la segunda ejecución.
        */
        if (
            cargando &&
            String(ultimoPartidoCargado) === String(partidoId)
        ) {
            return;
        }

        /*
        Si el partido ya fue cargado, tampoco volvemos
        a insertar los mismos jugadores.
        */
        if (
            partidoId &&
            String(ultimoPartidoCargado) === String(partidoId) &&
            jugadorSelect.options.length > 1
        ) {
            return;
        }

        jugadorActual = jugadorSelect.value || jugadorActual;

        jugadorSelect.innerHTML =
            '<option value="">---------</option>';

        if (!partidoId) {
            ultimoPartidoCargado = null;
            jugadorSelect.disabled = false;
            return;
        }

        cargando = true;
        ultimoPartidoCargado = partidoId;
        jugadorSelect.disabled = true;

        let url;

        if (
            window.location.pathname.includes(
                "/admin/estadisticas/gol/"
            )
        ) {
            url =
                "/admin/estadisticas/gol/" +
                "jugadores-por-partido/";
        } else if (
            window.location.pathname.includes(
                "/admin/estadisticas/tarjeta/"
            )
        ) {
            url =
                "/admin/estadisticas/tarjeta/" +
                "jugadores-por-partido/";
        } else {
            console.error(
                "No se pudo identificar si el formulario es de gol o tarjeta."
            );

            cargando = false;
            jugadorSelect.disabled = false;
            return;
        }

        try {
            const respuesta = await fetch(
                `${url}?partido_id=${encodeURIComponent(partidoId)}`,
                {
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                }
            );

            if (!respuesta.ok) {
                throw new Error(
                    `Error HTTP ${respuesta.status}`
                );
            }

            const datos = await respuesta.json();

            /*
            Siempre limpiamos antes de agregar.
            */
            jugadorSelect.innerHTML =
                '<option value="">---------</option>';

            /*
            Set garantiza que un jugador nunca se inserte
            dos veces, aunque la respuesta viniera duplicada.
            */
            const idsInsertados = new Set();

            datos.jugadores.forEach(function (jugador) {
                const jugadorId = String(jugador.id);

                if (idsInsertados.has(jugadorId)) {
                    return;
                }

                idsInsertados.add(jugadorId);

                const opcion = document.createElement("option");

                opcion.value = jugador.id;
                opcion.textContent = jugador.texto;

                if (
                    jugadorActual &&
                    jugadorId === String(jugadorActual)
                ) {
                    opcion.selected = true;
                }

                jugadorSelect.appendChild(opcion);
            });

        } catch (error) {
            console.error(
                "Error al cargar los jugadores:",
                error
            );

            /*
            Permitimos volver a intentar seleccionar
            el mismo partido si hubo un error.
            */
            ultimoPartidoCargado = null;
        } finally {
            cargando = false;
            jugadorSelect.disabled = false;
        }
    }

    /*
    Evento normal.
    */
    partidoSelect.addEventListener(
        "change",
        cargarJugadores
    );

    /*
    Evento de Select2 utilizado por autocomplete_fields.
    Conservamos este porque en la versión anterior
    sí hacía aparecer los jugadores.
    */
    if (window.django && window.django.jQuery) {
        window.django.jQuery(partidoSelect)
            .off("select2:select.jugadores")
            .on(
                "select2:select.jugadores",
                cargarJugadores
            );

        window.django.jQuery(partidoSelect)
            .off("select2:clear.jugadores")
            .on(
                "select2:clear.jugadores",
                cargarJugadores
            );
    }

    /*
    Para editar un gol o una tarjeta existente.
    */
    if (partidoSelect.value) {
        cargarJugadores();
    }
});