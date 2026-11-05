import csv
import json
import os
from pathlib import Path

# Subir dos niveles desde src/auditoria hasta la raíz del proyecto
directorio_actual = os.path.dirname(__file__)
directorio_raiz = os.path.dirname(os.path.dirname(directorio_actual))

# Ruta por defecto al JSON dentro de data
archivo_json = os.path.join(
    directorio_raiz,
    "data",
    "entrada_G3_mochila_20_nodos.json"
)


def obtener_nombre_corto_dataset(ruta_archivo=archivo_json):
    """Extrae una versión corta del nombre del dataset (ej. 'entrada_G3')."""
    stem = Path(ruta_archivo).stem
    partes = stem.split("_")
    if len(partes) >= 2:
        return f"{partes[0]}_{partes[1]}"
    return stem


def cargar_json(ruta_archivo=None):
    ruta = str(ruta_archivo) if ruta_archivo is not None else archivo_json

    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    universo = set()

    for riesgo in datos["categorias_riesgo"]:
        universo.add(riesgo["id"])

    interacciones = {}

    for etapa in datos["etapas"]:
        nombre = etapa["id"]

        riesgos = set(
            etapa["riesgos_cubiertos_auditoria_completa"]
        )

        interacciones[nombre] = riesgos

    return universo, interacciones


def factibilidad(universo, interacciones):
    """Verifica si la unión de todas las interacciones cubre el universo de riesgos."""
    union_total = set()

    for riesgos in interacciones.values():
        union_total.update(riesgos)

    return universo.issubset(union_total)


def obtener_ruta_resultados():
    ruta_resultados = os.path.join(
        directorio_raiz,
        "resultados_auditoria"
    )
    os.makedirs(ruta_resultados, exist_ok=True)
    return ruta_resultados


def guardar_metrica_csv(nombre_instancia, nombre_algoritmo, tiempo, valor):
    ruta_res = obtener_ruta_resultados()
    archivo_csv = os.path.join(ruta_res, "comparativa_rendimiento.csv")

    archivo_existe = os.path.exists(archivo_csv)

    with open(archivo_csv, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not archivo_existe:
            writer.writerow(["instancia", "algoritmo", "tiempo_segundos", "valor_obtenido"])
        writer.writerow([nombre_instancia, nombre_algoritmo, tiempo, valor])


def guardar_interacciones_detalle(nombre_instancia, nombre_algoritmo, interacciones):
    ruta_res = obtener_ruta_resultados()
    nombre_corto = obtener_nombre_corto_dataset(nombre_instancia)
    nombre_archivo = f"{nombre_corto}_{nombre_algoritmo}.json"
    ruta_json = os.path.join(ruta_res, nombre_archivo)

    datos = {
        "instancia": nombre_corto,
        "algoritmo": nombre_algoritmo,
        "interacciones": interacciones
    }

    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def registrar_resultado_auditoria(nombre_instancia, nombre_algoritmo, tiempo, seleccionadas):
    """Centraliza el guardado de métricas en CSV y el detalle de interacciones en JSON."""
    nombre_corto = obtener_nombre_corto_dataset(nombre_instancia)
    guardar_metrica_csv(nombre_corto, nombre_algoritmo, tiempo, len(seleccionadas))
    guardar_interacciones_detalle(nombre_corto, nombre_algoritmo, list(seleccionadas))
