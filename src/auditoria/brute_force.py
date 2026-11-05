# Verificación empírica: comparar los resultados del algoritmo voraz contra el óptimo obtenido mediante fuerza bruta en instancias pequeñas.


# Categorías que debemos cubrir
# universo = {"A", "B", "C", "D", "E"}

# # Interacciones disponibles
# interacciones = {
#     "I1": {"A", "B", "C"},
#     "I2": {"A", "B"},
#     "I3": {"C", "D"},
#     "I4": {"D", "E"}
# }import time
import time
from auditoria.utils import cargar_json, guardar_interacciones_detalle, guardar_metrica_csv

def fuerza_bruta(universo, interacciones):
  # Iniciar cronómetro para medir el tiempo de ejecución de fuerza bruta
  inicio_tiempo = time.time()

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

      print(combinacion, "->", cubiertas)

      # Comprobar si cubrimos todo el universo
      if universo.issubset(cubiertas):
        print("\nSOLUCIÓN ÓPTIMA ENCONTRADA")
        print("Interacciones:", combinacion)
        print("Cantidad:", k)

        # Calcular el tiempo transcurrido
        tiempo_fb = time.time() - inicio_tiempo

        # Métrica principal (tamaño de la solución óptima)
        valor_fb = len(combinacion)

        # Nombre de la instancia (puedes ajustarlo si prefieres pasar el nombre del archivo de forma dinámica)
        nombre_instancia = "datos_profe.json"

        # Guardar automáticamente los resultados usando tu módulo utils
        guardar_metrica_csv(
            nombre_instancia, "fuerza_bruta", tiempo_fb, valor_fb
        )
        guardar_interacciones_detalle(
            nombre_instancia, "fuerza_bruta", list(combinacion)
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


# Cargar datos y ejecutar el algoritmo de fuerza bruta
# universo, interacciones = cargar_json()
# fuerza_bruta(universo, interacciones)