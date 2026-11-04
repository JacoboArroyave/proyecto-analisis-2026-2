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
  domain/          modelos y validaciones del dominio
  application/     caso de uso de programacion dinamica
  infrastructure/  adaptador de lectura JSON
  presentation/    interfaz de linea de comandos
```

Las dependencias apuntan hacia adentro: la DP no conoce JSON ni la CLI, y los modelos no dependen de infraestructura. El puerto `ScenarioReader` define la lectura requerida por la aplicacion; `JsonScenarioReader` es su adaptador concreto.

## Ejecucion

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m ruta_optima.presentation.cli
python -m unittest discover -s tests -v
```

Sin argumentos, la aplicacion lee automaticamente `data/entrada_G3_mochila_20_nodos.json`. Tambien acepta otra ruta JSON como argumento. La salida contiene la duracion base y final, costo utilizado, etapas elegidas y la traza de cada celda de la tabla DP.

## Logging

Cada ejecucion escribe en `logs/ruta_optima.log`. El archivo usa formato timestamp, nivel, modulo y mensaje; conserva hasta tres archivos rotativos de 1 MB. La terminal muestra eventos `INFO` y el archivo conserva tambien los estados `DEBUG` de la tabla DP.

Para usar otro directorio:

```bash
python -m ruta_optima.presentation.cli --log-dir resultados/logs
```

## Complejidad

Para `n` etapas y presupuesto entero `B`, la tabla tiene `(n + 1)(B + 1)` estados y cada estado se calcula en tiempo constante. Por tanto:

- Tiempo: `O(n * B)`.
- Espacio: `O(n * B)` por la tabla de decisiones usada para reconstruir la solucion.

Es pseudo-polinomial: si `B` se representa en binario, el costo depende del valor numerico de `B`, no solo del numero de bits.

## Entrada oficial de G3

La entrada oficial `data/entrada_G3_mochila_20_nodos.json` contiene tambien datos de auditoria para la Parte 2. En este proyecto solo se leen `parametros.presupuesto_aceleracion_B` y los cuatro campos de aceleracion de cada objeto en `etapas`; los datos de riesgos y auditoria se ignoran porque corresponden al compañero encargado de esa parte.

```bash
python -m ruta_optima.presentation.cli data/entrada_G3_mochila_20_nodos.json > resultados/entrada_G3_parte1.json
```

La logica no necesita editarse para otros casos con el mismo formato y la salida se puede conservar como evidencia.