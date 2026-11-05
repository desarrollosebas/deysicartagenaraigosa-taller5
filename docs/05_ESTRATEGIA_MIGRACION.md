# 05 — Estrategia de Migración

---

## 1. Fuente de datos

- **Archivo**: `SEGUIMIENTO TEMPERAS Y VINILOS Actividad(1).xlsm`
- **Tabla principal**: `T_baseDeDatos` — 8,208 filas, 58 columnas
- **Tabla de subcódigos**: `Base_de_datos_subcodigos` — 1,252 filas, 19 columnas
- **Período**: 2022-01-01 a 2025-03-28

## 2. Proceso de extracción

1. El archivo XLSM se extrajo a CSV mediante lectura del paquete Office Open XML (sin ejecutar macros)
2. Se generaron CSVs por hoja y reportes de diagnóstico
3. Los archivos originales se conservan intactos en `insumos_originales/01_FUENTES_ORIGINALES/`

## 3. Transformaciones aplicadas

| Transformación | Descripción | Justificación |
|---------------|-------------|---------------|
| Pseudonimización de operarios | Nombres reales → pseudónimos OP-001 a OP-032 | Protección de datos personales (RN-011) |
| Pseudonimización de personal | Nombres reales → pseudónimos PM-001 a PM-NNN | Protección de datos personales |
| Normalización de códigos de paro | 18 columnas horizontales → filas en tabla detalle_paro | Eliminación de grupo repetitivo (1FN) |
| Eliminación de campos calculados | Mes, Año, Código N en horas → calculados con SQL | Eliminación de dependencias transitivas (3FN) |
| Normalización de catálogos | Texto libre → FK a tablas maestras | Integridad referencial |
| Turno vacío → "No aplica" | Campos vacíos de turno se asignan al turno "No aplica" | Coherencia de datos |
| Operario vacío → NULL | Campos vacíos se dejan como NULL en id_operario | Distinguir "no registrado" de "no aplica" |

## 4. Mapeo de datos

| Campo Excel | → | Tabla destino | Campo destino |
|------------|---|---------------|---------------|
| Fecha | → | registro_produccion | fecha |
| Maquina | → | registro_produccion | id_maquina (FK) |
| Turno | → | registro_produccion | id_turno (FK) |
| Operario | → | registro_produccion | id_operario (FK, pseudonimizado) |
| Referencia | → | registro_produccion | id_referencia (FK) |
| Horas trabajadas | → | registro_produccion | horas_trabajadas |
| Pacas producidas | → | registro_produccion | pacas_producidas |
| Horas no trabajadas | → | registro_produccion | horas_no_trabajadas |
| Tipo de paro | → | registro_produccion | id_tipo_paro (FK) |
| Observaciones de paro | → | registro_produccion | observaciones_paro |
| Tiempo de Paro | → | registro_produccion | tiempo_paro_minutos |
| Observaciones | → | registro_produccion | observaciones |
| Codigo de paro N (×18) | → | detalle_paro | duracion_minutos (1 fila por código > 0) |

## 5. Orden de carga

```
1. 00_crear_base_datos.sql     → Crea la base de datos
2. 01_crear_tablas.sql         → Crea el esquema completo
3. 02_datos_catalogos.sql      → Carga catálogos (máquinas, turnos, códigos, subcódigos, tipos)
4. 03_crear_indices.sql        → Crea índices de rendimiento
5. 04_datos_operarios.sql      → Carga operarios pseudonimizados
6. 05_datos_referencias.sql    → Carga catálogo de productos
7. 06_datos_registros.sql      → Carga los 8,208 registros de producción
8. 07_datos_detalles_paro.sql  → Carga los 16,532 detalles de paro
9. 07b_datos_subcodigos.sql    → Carga los 1,115 detalles de subcódigo
10. 08_consultas_negocio.sql   → Ejecuta las consultas de indicadores
11. 09_pruebas_restricciones.sql → Ejecuta pruebas de integridad
```

## 6. Archivo de pseudonimización

El mapeo `nombre_real → pseudónimo` se almacena en:
```
migration/scripts/MAPEO_PRIVADO_NO_PUBLICAR.csv
```

**Este archivo NO debe subirse al repositorio público.** Está incluido en el `.gitignore`.

Si la empresa necesita recuperar la identidad de un operario a partir de su pseudónimo, debe consultar este archivo localmente.

