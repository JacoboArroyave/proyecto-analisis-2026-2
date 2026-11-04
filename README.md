# Ruta optima - Grupo 3

Implementación del Subproyecto 3: **Ruta crítica con aceleración bajo presupuesto y cobertura mínima de auditoría**.

El proyecto completo contempla dos capacidades:

- **Aceleración óptima de la cadena bajo presupuesto:** selecciona las etapas que deben acelerarse para maximizar la reducción de tiempo sin superar el presupuesto.
- **Cobertura mínima de auditoría:** selecciona interacciones o etapas que cubran las categorías de riesgo requeridas.

Este repositorio ejecuta actualmente la primera capacidad, denominada **Aceleración óptima de la cadena bajo presupuesto**. La cobertura de auditoría se desarrolla en el módulo correspondiente del otro integrante y no se ejecuta mediante este CLI.

## Modelo de aceleración de la ruta crítica

Cada etapa `i` tiene:

- `duration` (`t_i`): duracion normal.
- `cost` (`c_i`): costo de acelerarla.
- `reduction` (`d_i`): reduccion de tiempo obtenida.

Dado un presupuesto `B`, se elige un subconjunto de etapas para maximizar `sum(d_i)` sujeto a `sum(c_i) <= B`.
La duración final es `sum(t_i) - sum(d_i)`. Este problema se resuelve exactamente como una mochila 0/1.

## Arquitectura

```text
src/ruta_optima/
  constants/      constantes globales de configuracion
  domain/          modelos y validaciones del dominio
  application/     caso de uso de programacion dinamica
  infrastructure/  adaptador de lectura JSON

src/main.py         punto de entrada principal de la CLI
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

La aplicación ejecuta la **Aceleración óptima de la cadena bajo presupuesto**, lee automáticamente `data/entrada_G3_mochila_20_nodos.json` y muestra un resumen conciso con resultados, tiempo de ejecución y cantidad de estados de la traza. Los datos de auditoría presentes en el JSON no son procesados por este comando.

Para imprimir tambien la traza completa:

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

La formalización, reducción de NP-dureza, recurrencia y análisis de complejidad están documentados en [demostracion_np_dureza.md](docs/demostracion_np_dureza.md). La arquitectura y el funcionamiento interno están descritos en [MANUAL_TECNICO.md](docs/MANUAL_TECNICO.md).

## Entrada oficial de G3

La entrada oficial `data/entrada_G3_mochila_20_nodos.json` contiene datos para las dos capacidades del Subproyecto 3. Este CLI extrae únicamente `parametros.presupuesto_aceleracion_B` y los cuatro campos de aceleración de cada objeto en `etapas` para ejecutar la **Aceleración óptima de la cadena bajo presupuesto**. Los datos de riesgos y auditoría quedan disponibles para el módulo del otro integrante.

```bash
python src/main.py data/entrada_G3_mochila_20_nodos.json > resultados/entrada_G3_aceleracion.json
```

La logica no necesita editarse para otros casos con el mismo formato y la salida se puede conservar como evidencia.