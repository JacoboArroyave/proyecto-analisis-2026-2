# Manual tecnico - Parte 1

## Entrada

Un archivo JSON con un entero `budget` y una lista `stages`. Cada etapa contiene `name`, `duration`, `cost` y `reduction`, todos enteros no negativos. La reduccion no puede ser mayor que la duracion.

## Salida

El programa imprime JSON con:

- `base_duration` y `total_duration`.
- `total_cost` y `total_reduction`.
- `accelerated_stages`.
- `accelerated_stage_details`, con nombre, costo y reduccion de cada etapa seleccionada.
- `dp_trace`, una entrada por estado calculado: etapa, presupuesto disponible, reduccion maxima y decision.

## Algoritmo

Para cada etapa y cada presupuesto `b`, se compara no tomarla con tomarla:

`DP[i][b] = max(DP[i-1][b], DP[i-1][b-c_i] + d_i)` cuando `c_i <= b`.

La reconstruccion recorre las etapas de atras hacia adelante y recupera las decisiones que forman la reduccion optima.

## Limites y supuestos

- Los costos y el presupuesto deben ser enteros para indexar la tabla.
- Todas las etapas estan en serie, por lo que la duracion de la cadena es la suma de sus duraciones.
- Cada etapa puede acelerarse como maximo una vez.
- Los casos oficiales se agregan como archivos de datos, sin cambiar el algoritmo.