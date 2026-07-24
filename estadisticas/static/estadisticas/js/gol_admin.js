document.addEventListener("DOMContentLoaded", function () {
    const partidoSelect = document.getElementById("id_partido");
    const jugadorSelect = document.getElementById("id_jugador");

    if (!partidoSelect || !jugadorSelect) {
        return;
    }

    let jugadorActual = jugadorSelect.value;
    let controlador = null;

    async function cargarJugadores() {
        const partidoId = partidoSelect.value;

        jugadorActual = jugadorSelect.value || jugadorActual;

        /*
        Cancela una petición anterior si el evento
        se ejecuta nuevamente antes de terminar.
        */
        if (controlador) {
            controlador.abort();
        }

        controlador = new AbortController();

        jugadorSelect.disabled = true;
        jugadorSelect.innerHTML =
            '<option value="">---------</option>';

        if (!partidoId) {
            jugadorSelect.disabled = false;
            return;
        }

        const url =
            "/admin/estadisticas/gol/jugadores-por-partido/" +
            `?partido_id=${encodeURIComponent(partidoId)}`;

        try {
            const respuesta = await fetch(url, {
                signal: controlador.signal,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            if (!respuesta.ok) {
                throw new Error(
                    `Error HTTP ${respuesta.status}`
                );
            }

            const datos = await respuesta.json();

            /*
            Volvemos a limpiar antes de agregar.
            Esto impide duplicados aunque se hayan
            disparado dos eventos.
            */
            jugadorSelect.innerHTML =
                '<option value="">---------</option>';

            datos.jugadores.forEach(function (jugador) {
                const opcion =
                    document.createElement("option");

                opcion.value = jugador.id;
                opcion.textContent = jugador.texto;

                if (
                    String(jugador.id) ===
                    String(jugadorActual)
                ) {
                    opcion.selected = true;
                }

                jugadorSelect.appendChild(opcion);
            });

        } catch (error) {
            if (error.name !== "AbortError") {
                console.error(
                    "No se pudieron cargar los jugadores:",
                    error
                );
            }
        } finally {
            jugadorSelect.disabled = false;
        }
    }

    /*
    Solo necesitamos un evento change.
    No agregues también select2:select porque
    provocaría dos cargas.
    */
    partidoSelect.addEventListener(
        "change",
        cargarJugadores
    );

    if (partidoSelect.value) {
        cargarJugadores();
    }
});