-- ============================================================================
-- 03_crear_indices.sql
-- Índices para optimizar las consultas de negocio
-- Ejecutar después de: 01_crear_tablas.sql
-- Motor: MySQL 8.x
-- ============================================================================

USE paros_produccion;

-- --------------------------------------------------------
-- Índice 1: Búsqueda de registros por fecha
-- Justificación: Todas las consultas de negocio filtran por rango de fechas
-- (productividad mensual, comparativos anuales, evolución temporal)
-- --------------------------------------------------------
CREATE INDEX idx_reg_fecha ON registro_produccion (fecha);

-- --------------------------------------------------------
-- Índice 2: Búsqueda de registros por máquina y fecha
-- Justificación: La consulta principal (productividad por máquina y mes)
-- agrupa por máquina y filtra por fecha simultáneamente
-- --------------------------------------------------------
CREATE INDEX idx_reg_maquina_fecha ON registro_produccion (id_maquina, fecha);

-- --------------------------------------------------------
-- Índice 3: Búsqueda de registros por turno
-- Justificación: La consulta de comparación de turnos agrupa por turno
-- --------------------------------------------------------
CREATE INDEX idx_reg_turno ON registro_produccion (id_turno);

-- --------------------------------------------------------
-- Índice 4: Búsqueda de detalle de paros por código
-- Justificación: Las consultas de participación porcentual de códigos
-- y análisis de subcódigos necesitan agrupar por código
-- --------------------------------------------------------
CREATE INDEX idx_dp_codigo ON detalle_paro (id_codigo);

-- --------------------------------------------------------
-- Índice 5: Búsqueda de detalle de subcódigos por subcódigo
-- Justificación: El análisis detallado de códigos 01, 03 y 05
-- necesita agrupar por subcódigo
-- --------------------------------------------------------
CREATE INDEX idx_ds_subcodigo ON detalle_subcodigo (id_subcodigo);

-- --------------------------------------------------------
-- Índice 6: Búsqueda de registros por operario
-- Justificación: Consultas de rendimiento por operario
-- --------------------------------------------------------
CREATE INDEX idx_reg_operario ON registro_produccion (id_operario);

