from time import perf_counter
from auditoria.utils import (
    archivo_json,
    factibilidad,
    registrar_resultado_auditoria,
)


def greedy(universo, interacciones, nombre_instancia=archivo_json):
    # Iniciar cronómetro para medir el tiempo de ejecución de greedy
    inicio_tiempo = perf_counter()

    # Verificar factibilidad antes de ejecutar
    if not factibilidad(universo, interacciones):
        print("INSTANCIA NO FACTIBLE")
        print("Existen categorías de riesgo sin cobertura.")
        return None

    print("INSTANCIA FACTIBLE")
    print("Todas las categorías tienen cobertura.\n")

    # Inicializar solución (lista para orden y set para búsqueda en O(1) promedio)
    cubiertas = set()
    seleccionadas = []
    seleccionadas_set = set()

    while not universo.issubset(cubiertas):
        mejor_interaccion = None
        mejores_nuevos = set()
        mejor_cantidad = 0

        # Buscar la interacción que cubra más riesgos nuevos
        for nombre, riesgos in interacciones.items():
            if nombre in seleccionadas_set:
                continue

            nuevos = riesgos - cubiertas
            cantidad = len(nuevos)

            if cantidad > mejor_cantidad:
                mejor_cantidad = cantidad
                mejor_interaccion = nombre
                mejores_nuevos = nuevos

        # Verificar que exista una interacción útil
        if mejor_interaccion is None:
            print("No fue posible completar la cobertura.")
            return None

        # Seleccionar interacción
        seleccionadas.append(mejor_interaccion)
        seleccionadas_set.add(mejor_interaccion)
        cubiertas.update(mejores_nuevos)

        print(
            f"Seleccionada: {mejor_interaccion} | "
            f"Nuevos riesgos: {mejores_nuevos} | "
            f"Total cubiertos: {cubiertas}"
        )

    print("\nSOLUCIÓN VORAZ ENCONTRADA")
    print("Interacciones:", seleccionadas)
    print("Cantidad:", len(seleccionadas))

    tiempo_greedy = perf_counter() - inicio_tiempo
    registrar_resultado_auditoria(
        nombre_instancia, "greedy", tiempo_greedy, seleccionadas
    )

    return seleccionadas
