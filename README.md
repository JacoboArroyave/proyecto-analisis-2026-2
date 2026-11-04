# Ruta optima - Grupo 3

Implementacion de la **Parte 1: aceleracion optima de una cadena bajo presupuesto**.
Este repositorio no incluye cobertura de auditoria, porque esa parte corresponde al otro integrante del equipo.

## Modelo

Cada etapa `i` tiene:

- `duration` (`t_i`): duracion normal.
- `cost` (`c_i`): costo de acelerarla.
- `reduction` (`d_i`): reduccion de tiempo obtenida.

Dado un presupuesto `B`, se elige un subconjunto de etapas para maximizar `sum(d_i)` sujeto a `sum(c_i) <= B`.
La duracion final es `sum(t_i) - sum(d_i)`. Es exactamente una mochila 0/1.

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

La aplicacion lee automaticamente `data/entrada_G3_mochila_20_nodos.json` y muestra un resumen conciso con resultados, tiempo de ejecucion y cantidad de estados de la traza.

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

## Complejidad

Para `n` etapas y presupuesto entero `B`, la tabla tiene `(n + 1)(B + 1)` estados y cada estado se calcula en tiempo constante. Por tanto:

- Tiempo: `O(n * B)`.
- Espacio: `O(n * B)` por la tabla de decisiones usada para reconstruir la solucion.

Es pseudo-polinomial: si `B` se representa en binario, el costo depende del valor numerico de `B`, no solo del numero de bits.

## Entrada oficial de G3

La entrada oficial `data/entrada_G3_mochila_20_nodos.json` contiene tambien datos de auditoria para la Parte 2. En este proyecto solo se leen `parametros.presupuesto_aceleracion_B` y los cuatro campos de aceleracion de cada objeto en `etapas`; los datos de riesgos y auditoria se ignoran porque corresponden al compañero encargado de esa parte.

```bash
python src/main.py data/entrada_G3_mochila_20_nodos.json > resultados/entrada_G3_parte1.json
```

La logica no necesita editarse para otros casos con el mismo formato y la salida se puede conservar como evidencia.