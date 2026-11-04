import time
from auditoria.utils import cargar_json, guardar_interacciones_detalle, guardar_metrica_csv

def factibilidad(universo, interacciones):
  union_total = set()

  for riesgos in interacciones.values():
    union_total.update(riesgos)

  return universo.issubset(union_total)


def greedy(universo, interacciones):
  # Iniciar cronómetro para medir el tiempo de ejecución de greedy
  inicio_tiempo = time.time()

  # Verificar factibilidad antes de ejecutar
  if not factibilidad(universo, interacciones):
    print("INSTANCIA NO FACTIBLE")
    print("Existen categorías de riesgo sin cobertura.")
    return None

  print("INSTANCIA FACTIBLE")
  print("Todas las categorías tienen cobertura.\n")

  # Inicializar solución
  cubiertas = set()
  seleccionadas = []

  while not universo.issubset(cubiertas):
    mejor_interaccion = None
    mejor_cantidad = 0

    # Buscar la interacción que cubra más riesgos nuevos
    for nombre, riesgos in interacciones.items():
      if nombre in seleccionadas:
        continue

      nuevos = riesgos - cubiertas
      cantidad = len(nuevos)

      if cantidad > mejor_cantidad:
        mejor_cantidad = cantidad
        mejor_interaccion = nombre

    # Verificar que exista una interacción útil
    if mejor_interaccion is None:
      print("No fue posible completar la cobertura.")
      return None

    # Seleccionar interacción
    seleccionadas.append(mejor_interaccion)

    nuevos = interacciones[mejor_interaccion] - cubiertas
    cubiertas.update(nuevos)

    print(
        f"Seleccionada: {mejor_interaccion} | "
        f"Nuevos riesgos: {nuevos} | "
        f"Total cubiertos: {cubiertas}"
    )

  print("\nSOLUCIÓN VORAZ ENCONTRADA")
  print("Interacciones:", seleccionadas)
  print("Cantidad:", len(seleccionadas))

  # Calcular el tiempo transcurrido
  tiempo_greedy = time.time() - inicio_tiempo

  # Definir el valor o métrica principal (por ejemplo, el tamaño de la solución o cantidad de interacciones)
  # Puedes cambiar len(seleccionadas) por el costo total u otra métrica si tu problema lo requiere.
  valor_greedy = len(seleccionadas)

  nombre_instancia = (
      "datos1.json"  # O puedes pasarlo dinámicamente si prefieres
  )

  # Guardar automáticamente los resultados usando tu módulo utils
  guardar_metrica_csv(nombre_instancia, "greedy", tiempo_greedy, valor_greedy)
  guardar_interacciones_detalle(
      nombre_instancia, "greedy", seleccionadas
  )

  return seleccionadas


# Cargar datos y ejecutar el algoritmo
# universo, interacciones = cargar_json()
# greedy(universo, interacciones)