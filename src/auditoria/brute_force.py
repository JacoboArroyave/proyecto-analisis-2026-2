# Verificación empírica: comparar los resultados del algoritmo voraz contra el óptimo obtenido mediante fuerza bruta en instancias pequeñas.

from time import perf_counter
from auditoria.utils import (
    archivo_json,
    factibilidad,
    registrar_resultado_auditoria,
)


def fuerza_bruta(universo, interacciones, nombre_instancia=archivo_json):
    # Iniciar cronómetro para medir el tiempo de ejecución de fuerza bruta
    inicio_tiempo = perf_counter()

    # Verificar factibilidad antes de explorar combinaciones
    if not factibilidad(universo, interacciones):
        print("INSTANCIA NO FACTIBLE")
        print("Existen categorías de riesgo sin cobertura.")
        return None

    nombres = list(interacciones.keys())
    n = len(nombres)

    # Todas las combinaciones ordenadas por tamaño (k)
    for k in range(1, n + 1):
        print(f"\nProbando combinaciones de tamaño {k}")

        for combinacion in combinaciones(nombres, k):
            # Unir las categorías cubiertas
            cubiertas = set()

            for nombre in combinacion:
                cubiertas.update(interacciones[nombre])

            # print(combinacion, "->", cubiertas)

            # Comprobar si cubrimos todo el universo
            if universo.issubset(cubiertas):
                print("\nSOLUCIÓN ÓPTIMA ENCONTRADA")
                print("Interacciones:", combinacion)
                print("Cantidad:", k)

                tiempo_fb = perf_counter() - inicio_tiempo
                registrar_resultado_auditoria(
                    nombre_instancia, "fuerza_bruta", tiempo_fb, combinacion
                )

                return combinacion

    print("No se encontró ninguna solución factible.")
    return None


def combinaciones(elementos, k):
    n = len(elementos)
    resultado = []

    def generar(inicio, actual):
        # Caso base: ya tenemos k elementos
        if len(actual) == k:
            resultado.append(actual.copy())
            return

        # Recorrer los elementos disponibles
        for i in range(inicio, n):
            actual.append(elementos[i])
            generar(i + 1, actual)
            actual.pop()

    generar(0, [])
    return resultado
