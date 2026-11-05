# Taller 5 — Base de Datos para Registro de Paros de Producción

## 📋 Información del proyecto

| Campo | Valor |
|-------|-------|
| **Asignatura** | Bases de Datos I |
| **Actividad** | Taller 5  |
| **Integrante 1** | Juan Sebastián Raigosa Gil (desarrollosebas) |
| **Integrante 2** | Deysi Carolina Echavarría Soto (CarolinaSoto22) |
| **Integrante 3** | Jose Miguel Sosa Cartagena (josesosa216-pb) |
| **Motor** | MySQL 8.x |
| **Herramienta** | DBeaver |
| **Repositorio** | [github.com/desarrollosebas/deysicartagenaraigosa-taller5](https://github.com/desarrollosebas/deysicartagenaraigosa-taller5) |

---

## 🎯 Objetivo

Diseñar, implementar y poblar una base de datos relacional normalizada que reemplace el libro Excel usado actualmente para registrar los paros de producción de las líneas de envasado de vinilos de una empresa fabricante de pinturas.

## 📖 Contexto del problema

La empresa opera **4 líneas de envasado** (Vinilos_1 a Vinilos_4) donde las operarias registran manualmente la producción y los paros en un formato "hora a hora". Esta información se transcribe a un libro Excel con macros que almacena más de **8,200 registros históricos** (2022-2025) y genera indicadores de productividad.

El Excel presenta problemas de:
- Grupos de columnas repetidas (18 códigos × 2 columnas)
- Ausencia de integridad referencial
- Redundancia de datos calculados
- Dependencia de macros VBA para validaciones
- Dificultad para consultar históricos

La base de datos relacional resuelve estos problemas mediante normalización a **3FN**, catálogos con integridad referencial y consultas SQL estructuradas.

## 🗂️ Estructura del repositorio

```
├── README.md                          ← Este archivo
├── .gitignore                         ← Archivos excluidos del repositorio
├── docs/
│   ├── 00_AUDITORIA_INSUMOS.md       ← Inventario y análisis de archivos fuente
│   ├── 01_REGLAS_NEGOCIO.md          ← 48 reglas de negocio identificadas
│   ├── 02_DIAGNOSTICO_NORMALIZACION.md ← Diagnóstico del Excel + normalización 1FN→3FN
│   ├── 03_DICCIONARIO_DATOS.md       ← Diccionario de datos completo (11 tablas)
│   ├── 04_DISENO_FISICO.md           ← Modelo ER, justificación de índices y FK
│   ├── 05_ESTRATEGIA_MIGRACION.md    ← Plan de migración del Excel
│   ├── 06_VALIDACION_MIGRACION.md    ← Reporte cuantitativo de la migración
│   ├── 07_INDICADORES_Y_CONSULTAS.md ← Fórmulas de productividad y catálogo de consultas
│   ├── 08_PRUEBAS_Y_VALIDACION.md    ← Plan de pruebas y procedimiento de ejecución
│   ├── 09_GUIA_SUSTENTACION.md       ← Guía para defender el proyecto
│   └── modelo/
│       ├── 01_modelo_conceptual.md   ← Modelo entidad-relación conceptual
│       ├── 02_modelo_logico.md       ← Modelo relacional lógico
│       └── 03_modelo_fisico.md       ← Diseño físico completo
├── sql/
│   ├── 00_crear_base_datos.sql       ← Crea la base de datos
│   ├── 01_crear_tablas.sql           ← Crea las 11 tablas con restricciones
│   ├── 02_datos_catalogos.sql        ← Catálogos: máquinas, turnos, códigos, subcódigos
│   ├── 03_crear_indices.sql          ← 6 índices justificados
│   ├── 04_datos_operarios.sql        ← Operarios pseudonimizados
│   ├── 05_datos_referencias.sql      ← Catálogo de productos
│   ├── 06_datos_registros.sql        ← 8,208 registros de producción migrados
│   ├── 07_datos_detalles_paro.sql    ← 16,532 detalles de paro
│   ├── 07b_datos_subcodigos.sql      ← 1,115 detalles de subcódigo
│   ├── 08_consultas_negocio.sql      ← 10 consultas de indicadores
│   └── 09_pruebas_restricciones.sql  ← Pruebas de INSERT, UPDATE, DELETE y rechazos
├── migration/
│   └── scripts/
│       └── 04_migrar_datos.py        ← Script de migración (Python)
└── report/
    ├── BDI_ProyectoFinal_Raigosa_Echavarria.pdf
    └── BDI_ProyectoFinal_Raigosa_Echavarria_Sosa.pdf
```

## 🚀 Cómo ejecutar desde cero en DBeaver

### Requisitos
- MySQL 8.x instalado y en ejecución
- DBeaver instalado y conectado a MySQL

### Pasos

1. **Abrir DBeaver** y conectar a la instancia MySQL local
2. Ejecutar los scripts SQL **en orden** (del 00 al 09):

```
sql/00_crear_base_datos.sql    → Crea la base de datos
sql/01_crear_tablas.sql        → Crea el esquema
sql/02_datos_catalogos.sql     → Carga catálogos
sql/03_crear_indices.sql       → Crea índices
sql/04_datos_operarios.sql     → Carga operarios
sql/05_datos_referencias.sql   → Carga productos
sql/06_datos_registros.sql     → Carga registros históricos
sql/07_datos_detalles_paro.sql → Carga detalles de paro
sql/07b_datos_subcodigos.sql   → Carga detalles de subcódigo
sql/08_consultas_negocio.sql   → Ejecuta consultas de negocio
sql/09_pruebas_restricciones.sql → Ejecuta pruebas
```

3. Para ejecutar en DBeaver: abrir cada archivo → Ctrl+Enter o Alt+X

## 📊 Modelo de datos

El esquema tiene **11 tablas** normalizadas hasta **3FN**:

- **5 tablas de catálogo**: maquina, turno, operario, referencia, codigo_paro
- **2 tablas de relación**: referencia_maquina, subcodigo_paro
- **1 tabla de clasificación**: tipo_paro
- **1 tabla de hechos**: registro_produccion
- **2 tablas de detalle**: detalle_paro, detalle_subcodigo

## 🔒 Protección de datos personales

Los nombres reales de operarios y personal de mantenimiento han sido **pseudonimizados**:
- Operarios → OP-001, OP-002, ..., OP-032
- El mapeo real↔pseudónimo se almacena localmente y **no se publica** en el repositorio

## 📈 Consultas implementadas

1. Productividad por máquina y mes (comparativo anual)
2. Participación porcentual de cada código de paro
3. Análisis detallado de subcódigos 01, 03 y 05
4. Comparación del desempeño entre turnos
5. Máquinas con mayor tiempo de paro
6. Evolución mensual de tiempos de paro
7. Causas de paro más frecuentes (Top 10)
8. Producción real vs meta
9. Distribución de paros por área de impacto
10. Operarios con registros sin producción

