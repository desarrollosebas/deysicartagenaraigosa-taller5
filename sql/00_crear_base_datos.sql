-- ============================================================================
-- 00_crear_base_datos.sql
-- Crea la base de datos para el registro de paros de producción
-- Motor: MySQL 8.x
-- Proyecto: Taller 5 — BDI
-- ============================================================================

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS paros_produccion
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Seleccionar la base de datos
USE paros_produccion;

