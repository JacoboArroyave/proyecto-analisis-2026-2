# Ruta optima - Grupo 3

Implementación del Subproyecto 3: **Ruta crítica con aceleración bajo presupuesto y cobertura mínima de auditoría**.

El proyecto completo contempla dos capacidades integradas en el menú principal de la CLI:

- **Aceleración óptima de la cadena bajo presupuesto (Parte 1):** selecciona las etapas que deben acelerarse para maximizar la reducción de tiempo sin superar el presupuesto.
- **Cobertura mínima de auditoría (Parte 2):** selecciona el menor subconjunto de interacciones o etapas que cubra todas las categorías de riesgo normativo requeridas (mediante fuerza bruta exacta y aproximación voraz).

## Modelo de aceleración de la ruta crítica (Parte 1)

Cada etapa `i` tiene:

- `duration` (`t_i`): duracion normal.
- `cost` (`c_i`): costo de acelerarla.
- `reduction` (`d_i`): reduccion de tiempo obtenida.

Dado un presupuesto `B`, se elige un subconjunto de etapas para maximizar `sum(d_i)` sujeto a `sum(c_i) <= B`.
La duración final es `sum(t_i) - sum(d_i)`. Este problema se resuelve exactamente como una mochila 0/1.

## Modelo de cobertura mínima de auditoría (Parte 2)

Dado un universo de `r` categorías de riesgo (`categorias_riesgo`) y `n` etapas candidatas donde cada etapa cubre un subconjunto de categorías (`riesgos_cubiertos_auditoria_completa`), se busca el subconjunto de etapas de cardinalidad mínima cuya unión cubra las `r` categorías. Corresponde al problema clásico *Set Cover* y se resuelve de forma exacta (fuerza bruta) y aproximada (algoritmo voraz con cota armónica `H_r`).

## Arquitectura

```text
src/ruta_optima/
  constants/      constantes globales de configuracion
  domain/          modelos y validaciones del dominio
  application/     caso de uso de programacion dinamica
  infrastructure/  adaptador de lectura JSON

src/auditoria/
  brute_force.py   algoritmo exacto de cobertura por fuerza bruta
  greedy.py        algoritmo aproximado voraz (Set Cover)
  utils.py         carga de datos, factibilidad y guardado en resultados_auditoria/

src/main.py         punto de entrada principal con menu interactivo (Partes 1 y 2)
```

Las dependencias apuntan hacia adentro: la DP no conoce JSON ni la CLI, y los modelos no dependen de infraestructura. Las constantes globales viven en `constants/base.py`. El puerto `ScenarioReader` define la lectura requerida por la aplicacion; `JsonScenarioReader` es su adaptador concreto.

## Manual de usuario

### Requisitos

- Python 3.10 o superior.
- Git.
- Linux, macOS o Windows.

### Instalacion

```bash
git clone https://github.com/JacoboArroyave/proyecto-analisis-2026-2.git
cd proyecto-analisis-2026-2
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

En Windows PowerShell, activar el entorno con `.venv\\Scripts\\Activate.ps1`.

### Ejecucion

Desde la raiz del proyecto:

```bash
python src/main.py
```

Al ejecutar `python src/main.py`, se despliega el menú interactivo desde el cual se pueden ejecutar ambas partes sobre `data/entrada_G3_mochila_20_nodos.json`:

- **Opción 1 (Aceleración óptima de la cadena bajo presupuesto):** ejecuta la programación dinámica, muestra el resumen conciso con resultados, tiempo de ejecución y cantidad de estados de la traza.
- **Opción 2 (Fuerza Bruta - Auditoría):** encuentra la cobertura mínima exacta y registra la salida en `resultados_auditoria/entrada_G3_fuerza_bruta.json` y en `resultados_auditoria/comparativa_rendimiento.csv`.
- **Opción 3 (Greedy / Voraz - Auditoría):** ejecuta la aproximación voraz y registra la salida en `resultados_auditoria/entrada_G3_greedy.json` y en `resultados_auditoria/comparativa_rendimiento.csv`.

Para imprimir tambien la traza completa de la Parte 1:

```bash
python src/main.py --full-output
```

## Logging

Cada ejecución escribe un archivo histórico en `logs/DD_MM_YYYY/HHhrs/ruta_optima.log` y sobrescribe `logs/last_ruta_optima.log` con la ejecución más reciente. La consola muestra eventos `INFO` con color cuando `colorama` está instalada; el archivo conserva también los estados `DEBUG` de la tabla DP.

Para usar otro directorio de logs:

```bash
python src/main.py --log-dir resultados/logs
```

Los logs se guardan en `logs/DD_MM_YYYY/HHhrs/ruta_optima.log` y en `logs/last_ruta_optima.log`. La consola muestra eventos con color cuando `colorama` esta disponible; los archivos permanecen sin colores.

## Análisis técnico

La formalización, reducción de NP-dureza, recurrencia y análisis de complejidad están documentados en `formalizacion_mochila` (Parte 1) y `formalizacion_set_cover` (Parte 2). La arquitectura y el funcionamiento interno están descritos en `MANUAL_TECNICO`.

## Entrada oficial de G3

La entrada oficial `data/entrada_G3_mochila_20_nodos.json` contiene datos para las dos capacidades del Subproyecto 3:
- **Parte 1 (Aceleración):** consume `parametros.presupuesto_aceleracion_B` y los atributos de duración, costo y reducción de cada objeto en `etapas`.
- **Parte 2 (Auditoría):** consume `categorias_riesgo` y `riesgos_cubiertos_auditoria_completa` de cada etapa, guardando automáticamente las métricas y selecciones en `resultados_auditoria/`.

```bash
python src/main.py data/entrada_G3_mochila_20_nodos.json > resultados/entrada_G3_aceleracion.json
```

La logica no necesita editarse para otros casos con el mismo formato y la salida se puede conservar como evidencia.