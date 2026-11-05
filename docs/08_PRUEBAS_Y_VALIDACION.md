# 08 — Pruebas y Validación

---

## 1. Procedimiento para ejecutar desde DBeaver

### Requisitos previos
- MySQL 8.x instalado y en ejecución
- DBeaver conectado a la instancia MySQL
- Carpeta `sql/` disponible con todos los scripts

### Orden de ejecución

1. Abrir DBeaver → conectar a MySQL
2. Ejecutar los scripts **en este orden exacto**:

| Paso | Script | Qué hace |
|------|--------|----------|
| 1 | `00_crear_base_datos.sql` | Crea la base `paros_produccion` |
| 2 | `01_crear_tablas.sql` | Crea las 11 tablas con restricciones |
| 3 | `02_datos_catalogos.sql` | Carga catálogos (máquinas, turnos, códigos, subcódigos) |
| 4 | `03_crear_indices.sql` | Crea los 6 índices de rendimiento |
| 5 | `04_datos_operarios.sql` | Carga 32 operarios pseudonimizados |
| 6 | `05_datos_referencias.sql` | Carga 51 referencias de productos |
| 7 | `06_datos_registros.sql` | Carga 8,208 registros de producción |
| 8 | `07_datos_detalles_paro.sql` | Carga 16,532 detalles de paro |
| 9 | `07b_datos_subcodigos.sql` | Carga 1,115 detalles de subcódigo |
| 10 | `08_consultas_negocio.sql` | Ejecuta las 10 consultas de indicadores |
| 11 | `09_pruebas_restricciones.sql` | Ejecuta las pruebas de integridad |

### Cómo ejecutar en DBeaver
1. Abrir el script SQL en DBeaver (File → Open File)
2. Seleccionar la conexión MySQL
3. Ejecutar con Ctrl+Enter (sentencia individual) o Alt+X (todo el script)

---

## 2. Pruebas de estructura

| Prueba | Verificación | Resultado esperado |
|--------|-------------|-------------------|
| Creación de base | `SHOW DATABASES LIKE 'paros_produccion'` | 1 fila |
| Tablas creadas | `SHOW TABLES` | 11 tablas |
| Claves primarias | `SHOW INDEX FROM registro_produccion WHERE Key_name = 'PRIMARY'` | id_registro |
| Claves foráneas | `SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_TYPE = 'FOREIGN KEY'` | 12 FK |
| Restricciones CHECK | `SELECT * FROM INFORMATION_SCHEMA.CHECK_CONSTRAINTS` | 8+ restricciones |
| Restricciones UNIQUE | `SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_TYPE = 'UNIQUE'` | 8 UNIQUE |

## 3. Pruebas de datos

| Prueba | Consulta de verificación | Valor esperado |
|--------|-------------------------|----------------|
| Total registros | `SELECT COUNT(*) FROM registro_produccion` | 8,208 |
| Total detalles de paro | `SELECT COUNT(*) FROM detalle_paro` | 16,532 |
| Total detalles subcódigo | `SELECT COUNT(*) FROM detalle_subcodigo` | 1,115 |
| Máquinas | `SELECT COUNT(*) FROM maquina` | 4 |
| Turnos | `SELECT COUNT(*) FROM turno` | 7 |
| Operarios | `SELECT COUNT(*) FROM operario` | 32 |
| Referencias | `SELECT COUNT(*) FROM referencia` | 51 |
| Códigos de paro | `SELECT COUNT(*) FROM codigo_paro` | 18 |
| Subcódigos de paro | `SELECT COUNT(*) FROM subcodigo_paro` | 47 |
| Tipos de paro | `SELECT COUNT(*) FROM tipo_paro` | 19 |
| Distribución Vinilos_1 | `SELECT COUNT(*) FROM registro_produccion WHERE id_maquina = 1` | 1,877 |
| Distribución Vinilos_2 | `SELECT COUNT(*) FROM registro_produccion WHERE id_maquina = 2` | 1,255 |
| Distribución Vinilos_3 | `SELECT COUNT(*) FROM registro_produccion WHERE id_maquina = 3` | 2,491 |
| Distribución Vinilos_4 | `SELECT COUNT(*) FROM registro_produccion WHERE id_maquina = 4` | 2,585 |
| Rango de fechas | `SELECT MIN(fecha), MAX(fecha) FROM registro_produccion` | 2022-01-01 a 2025-03-28 |

## 4. Pruebas de restricciones

Las pruebas están documentadas en `09_pruebas_restricciones.sql`. Resumen:

| # | Tipo | Descripción | Error esperado |
|---|------|-------------|----------------|
| 4.1 | UNIQUE | Máquina duplicada | Error 1062 |
| 4.2 | FK | Máquina inexistente | Error 1452 |
| 4.3 | CHECK | Factor negativo | Error 3819 |
| 4.4 | CHECK | Horas negativas | Error 3819 |
| 4.5 | RESTRICT | Borrar máquina con datos | Error 1451 |
| 4.6 | CHECK | Código fuera de rango 1-18 | Error 3819 |
| 4.7 | CHECK | Duración negativa | Error 3819 |

## 5. Pruebas de integridad referencial

| Verificación | Consulta | Resultado esperado |
|-------------|----------|-------------------|
| Sin FK huérfanas en detalle_paro | Sección 5.2 del script 09 | 0 encontradas |
| Sin máquinas inexistentes | Sección 5.3 del script 09 | 0 encontradas |
| Distribución coincide con Excel | Sección 5.4 del script 09 | Mismos conteos que FRECUENCIA_MAQUINAS.csv |

## 6. Estado de las pruebas

> **NOTA**: Las pruebas están diseñadas y documentadas. Su ejecución real requiere una instancia MySQL activa conectada desde DBeaver. Los resultados presentados son los esperados; la confirmación se realizará durante la sustentación ejecutando los scripts en vivo.

