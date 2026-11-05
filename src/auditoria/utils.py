import csv
import json
import os

directorio_actual = os.path.dirname(__file__)
archivo_json = os.path.join(directorio_actual, "datos1.json")

# Subir dos niveles hasta la raíz del proyecto
directorio_raiz = os.path.dirname(os.path.dirname(directorio_actual))

# Acceder al JSON dentro de data
archivo_json = os.path.join(
    directorio_raiz,
    "data",
    "entrada_G3_mochila_20_nodos.json"
)


def cargar_json():

    with open(archivo_json, "r", encoding="utf-8") as archivo:
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

def obtener_ruta_resultados():
    ruta_resultados = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
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
    nombre_archivo = f"{nombre_instancia}_{nombre_algoritmo}_interacciones.json"
    ruta_json = os.path.join(ruta_res, nombre_archivo)
    
    datos = {
        "instancia": nombre_instancia,
        "algoritmo": nombre_algoritmo,
        "interacciones": interacciones
    }
    
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)