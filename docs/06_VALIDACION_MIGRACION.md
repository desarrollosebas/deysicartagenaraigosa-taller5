# 06 — Validación de la Migración

---

## 1. Resumen cuantitativo

| Métrica | Valor |
|---------|-------|
| Total filas origen — tabla principal (CSV) | 8,208 |
| Registros procesados | 8,208 |
| Registros cargados exitosamente | 8,208 |
| Registros rechazados | 0 |
| Detalles de paro generados | 16,532 |
| Total filas origen — tabla subcódigos (CSV) | 1,252 |
| Subcódigos migrados | 1,115 |
| Registros padre no encontrados para subcódigos | 4 |
| Operarios únicos identificados | 32 |
| Referencias únicas | 51 |
| Tipos de paro únicos | 19 |

## 2. Verificación de integridad

| Verificación | Método | Resultado esperado |
|-------------|--------|-------------------|
| Conteo por máquina coincide | Comparar con FRECUENCIA_MAQUINAS.csv | Vinilos_1: 1877, V2: 1255, V3: 2491, V4: 2585 |
| Rango de fechas | MIN/MAX de fecha | 2022-01-01 a 2025-03-28 |
| Sin FK huérfanas | LEFT JOIN con tablas padre | 0 registros huérfanos |
| Total detalles > 0 corresponde | Sumar códigos no-cero del Excel | ≈16,532 |

## 3. Pseudonimización

- Se asignaron pseudónimos **OP-001** a **OP-032** a los 32 operarios únicos
- Personal de mantenimiento referenciado como **PM-ANON**
- El mapeo `nombre_real → pseudónimo` se almacena en:
  ```
  migration/scripts/MAPEO_PRIVADO_NO_PUBLICAR.csv
  ```
- Este archivo **NO debe subirse** al repositorio público
- Está incluido en el `.gitignore`

## 4. Registros no migrados

### Tabla principal
- **0 registros rechazados**: todas las 8,208 filas tenían fecha y máquina válida.

### Tabla de subcódigos
- **4 registros padre no encontrados**: el subcódigo hacía referencia a una combinación (fecha, máquina, turno, operario) que no existía como fila exacta en la tabla principal. Estos representan el 0.3% del total y no afectan la integridad del conjunto.
- **137 filas sin subcódigo informado**: estas filas del CSV de subcódigos tenían todos los campos de subcódigo vacíos (filas contextuales sin dato de paro). Se excluyeron correctamente.

## 5. Archivos generados

| Archivo | Contenido | Tamaño |
|---------|-----------|--------|
| `sql/04_datos_operarios.sql` | 32 operarios pseudonimizados | 1.8 KB |
| `sql/05_datos_referencias.sql` | 51 referencias de productos | 3.5 KB |
| `sql/06_datos_registros.sql` | 8,208 registros de producción | 809 KB |
| `sql/07_datos_detalles_paro.sql` | 16,532 detalles de paro | 301 KB |
| `sql/07b_datos_subcodigos.sql` | 1,115 detalles de subcódigo | ~50 KB |
| `migration/scripts/MAPEO_PRIVADO_NO_PUBLICAR.csv` | Mapeo de pseudónimos (PRIVADO) | 0.8 KB |
