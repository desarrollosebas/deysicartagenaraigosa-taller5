# 07 — Indicadores y Consultas de Negocio

---

## 1. Indicador principal: Productividad (%)

| Atributo | Detalle |
|----------|---------|
| **Nombre** | Porcentaje de productividad |
| **Propósito** | Medir la eficiencia de cada línea de envasado |
| **Fórmula** | `% Productividad = 100% − (Σ minutos_paro / (horas_trabajadas × 60)) × 100` |
| **Datos necesarios** | horas_trabajadas, duracion_minutos de cada código de paro |
| **Agrupación** | Por máquina, por mes, por año |
| **Unidad** | Porcentaje (0% a 100%) |
| **Inclusión** | Solo registros con horas_trabajadas > 0 |
| **Nulos/Cero** | Si horas_trabajadas = 0, se excluye del cálculo (evitar división por cero) |
| **Consulta SQL** | Consulta 1 en `08_consultas_negocio.sql` |

> **Nota**: La fórmula original del Excel usa `(pacas_producidas / produccion_ideal) × factor_produccion`. Dado que `meta_por_hora` no siempre está disponible en los datos migrados, se propone la fórmula alternativa basada en tiempos de paro, que es coherente con el gráfico de "% Códigos de paro" del PDF (donde la suma de los porcentajes de paro + productividad = 100%).

---

## 2. Catálogo de consultas

| # | Nombre | Pregunta del negocio | Requisitos SQL | Consulta |
|---|--------|---------------------|----------------|----------|
| 1 | Productividad por máquina y mes | ¿Cuál es el % de productividad de cada máquina por mes? | INNER JOIN, SUM, GROUP BY, BETWEEN, subconsulta | `08_consultas_negocio.sql` |
| 2 | Participación de códigos de paro | ¿Cuánto representa cada código en el total de paros? | INNER JOIN, SUM, GROUP BY, subconsulta | `08_consultas_negocio.sql` |
| 3 | Análisis de subcódigos 01, 03, 05 | ¿Cuáles son las causas específicas de estos paros? | INNER JOIN (×3), SUM, COUNT, GROUP BY, HAVING | `08_consultas_negocio.sql` |
| 4 | Comparación de turnos | ¿Qué turno tiene mejor productividad? | INNER JOIN, LEFT JOIN, AVG, COUNT, GROUP BY | `08_consultas_negocio.sql` |
| 5 | Máquinas con más paro | ¿Cuál máquina acumula más tiempo de paro? | INNER JOIN (×2), SUM, GROUP BY | `08_consultas_negocio.sql` |
| 6 | Evolución mensual de paros | ¿Cómo evolucionan los paros mes a mes? | JOIN, SUM, COUNT, GROUP BY, BETWEEN | `08_consultas_negocio.sql` |
| 7 | Causas más frecuentes | ¿Cuáles paros ocurren con más frecuencia? | INNER JOIN, COUNT, AVG, GROUP BY, HAVING | `08_consultas_negocio.sql` |
| 8 | Producción real vs meta | ¿Qué máquinas cumplen la meta? | INNER JOIN, AVG, GROUP BY, HAVING, subconsulta | `08_consultas_negocio.sql` |
| 9 | Paros por área de impacto | ¿Qué área genera más tiempo de paro? | INNER JOIN, SUM, GROUP BY, subconsulta | `08_consultas_negocio.sql` |
| 10 | Operarios sin producción | ¿Cuántos turnos tuvo cada operario sin producción? | LEFT JOIN, COUNT, SUM, GROUP BY, HAVING | `08_consultas_negocio.sql` |

## 3. Cobertura de requisitos SQL

| Requisito | Consultas donde se usa |
|-----------|----------------------|
| INNER JOIN | 1, 2, 3, 4, 5, 6, 7, 8, 9 |
| LEFT JOIN | 4, 10 |
| COUNT | 3, 4, 5, 6, 7, 10 |
| SUM | 1, 2, 3, 4, 5, 6, 9 |
| AVG | 4, 7, 8 |
| GROUP BY | Todas (1-10) |
| HAVING | 3, 7, 8, 10 |
| Subconsultas | 1, 2, 3, 8, 9 |
| BETWEEN (fechas) | 1, 6 |

