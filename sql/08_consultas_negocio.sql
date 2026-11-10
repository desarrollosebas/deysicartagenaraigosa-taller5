-- ============================================================================
-- 08_consultas_negocio.sql
-- Consultas SQL que responden preguntas reales del negocio
-- Motor: MySQL 8.x
-- ============================================================================

USE paros_produccion;

-- ============================================================================
-- CONSULTA 1: PRODUCTIVIDAD POR MÁQUINA Y MES (con comparativo anual)
-- ============================================================================
-- Pregunta: ¿Cuál es el porcentaje de productividad de cada máquina por mes?
--           ¿Cómo se compara entre años?
-- Requisitos SQL demostrados: INNER JOIN, funciones de agregación (SUM),
--   GROUP BY, filtro por rango de fechas (BETWEEN)
-- Fórmula: % Productividad = 100% - (Σ minutos_paro / (horas_trabajadas × 60)) × 100
-- ============================================================================

SELECT 
    m.nombre AS maquina,
    YEAR(rp.fecha) AS anio,
    MONTH(rp.fecha) AS mes,
    ROUND(SUM(rp.horas_trabajadas), 1) AS total_horas_trabajadas,
    ROUND(SUM(rp.pacas_producidas), 0) AS total_pacas,
    ROUND(SUM(dp_total.total_paro_min), 1) AS total_minutos_paro,
    ROUND(
        100 - (SUM(dp_total.total_paro_min) / NULLIF(SUM(rp.horas_trabajadas) * 60, 0)) * 100
    , 1) AS porcentaje_productividad
FROM registro_produccion rp
INNER JOIN maquina m ON rp.id_maquina = m.id_maquina
LEFT JOIN (
    -- Subconsulta: total de minutos de paro por registro
    SELECT id_registro, SUM(duracion_minutos) AS total_paro_min
    FROM detalle_paro
    GROUP BY id_registro
) dp_total ON rp.id_registro = dp_total.id_registro
WHERE rp.horas_trabajadas > 0
  AND rp.fecha BETWEEN '2024-01-01' AND '2025-12-31'
GROUP BY m.nombre, YEAR(rp.fecha), MONTH(rp.fecha)
ORDER BY m.nombre, anio, mes;


-- ============================================================================
-- CONSULTA 2: PARTICIPACIÓN PORCENTUAL DE CADA CÓDIGO DE PARO
-- ============================================================================
-- Pregunta: ¿Cuánto representa cada código en el total de tiempo de paro?
-- Requisitos SQL demostrados: INNER JOIN, SUM, GROUP BY, subconsulta
-- ============================================================================

SELECT 
    cp.numero AS codigo,
    cp.descripcion,
    cp.area_impacto,
    ROUND(SUM(dp.duracion_minutos), 1) AS total_minutos,
    ROUND(SUM(dp.duracion_minutos) / 60, 1) AS total_horas,
    ROUND(
        SUM(dp.duracion_minutos) / (
            SELECT SUM(duracion_minutos) FROM detalle_paro WHERE duracion_minutos > 0
        ) * 100
    , 2) AS porcentaje_del_total
FROM detalle_paro dp
INNER JOIN codigo_paro cp ON dp.id_codigo = cp.id_codigo
WHERE dp.duracion_minutos > 0
GROUP BY cp.numero, cp.descripcion, cp.area_impacto
ORDER BY total_minutos DESC;


-- ============================================================================
-- CONSULTA 3: ANÁLISIS DETALLADO POR SUBCÓDIGO (CÓDIGOS 01, 03 Y 05)
-- ============================================================================
-- Pregunta: ¿Cuáles son las causas específicas de los paros por falla
--           electromecánica (01), novedad de potencia (03) y ajuste operativo (05)?
-- Requisitos SQL demostrados: INNER JOIN (múltiple), SUM, GROUP BY, HAVING
-- ============================================================================

-- 3A: Subcódigos del código 01 - Falla electromecánica
SELECT 
    cp.numero AS codigo_padre,
    sp.codigo AS subcodigo,
    sp.descripcion AS causa_especifica,
    COUNT(*) AS frecuencia,
    ROUND(SUM(ds.duracion_minutos), 1) AS total_minutos,
    ROUND(SUM(ds.duracion_minutos) / 60, 2) AS total_horas,
    ROUND(
        SUM(ds.duracion_minutos) / NULLIF((
            SELECT SUM(ds2.duracion_minutos) 
            FROM detalle_subcodigo ds2
            INNER JOIN subcodigo_paro sp2 ON ds2.id_subcodigo = sp2.id_subcodigo
            WHERE sp2.id_codigo_padre = cp.id_codigo
        ), 0) * 100
    , 1) AS porcentaje_dentro_codigo
FROM detalle_subcodigo ds
INNER JOIN subcodigo_paro sp ON ds.id_subcodigo = sp.id_subcodigo
INNER JOIN codigo_paro cp ON sp.id_codigo_padre = cp.id_codigo
WHERE cp.numero IN (1, 3, 5)
GROUP BY cp.numero, cp.id_codigo, sp.codigo, sp.descripcion
HAVING SUM(ds.duracion_minutos) > 0
ORDER BY cp.numero, total_minutos DESC;


-- ============================================================================
-- CONSULTA 4: COMPARACIÓN DEL DESEMPEÑO ENTRE TURNOS
-- ============================================================================
-- Pregunta: ¿Qué turno tiene mejor productividad? ¿Cuál tiene más paros?
-- Requisitos SQL demostrados: INNER JOIN, LEFT JOIN, AVG, SUM, COUNT, GROUP BY
-- ============================================================================

SELECT 
    t.nombre AS turno,
    COUNT(DISTINCT rp.id_registro) AS total_registros,
    ROUND(AVG(rp.horas_trabajadas), 1) AS promedio_horas_trabajadas,
    ROUND(AVG(rp.pacas_producidas), 0) AS promedio_pacas,
    ROUND(SUM(rp.pacas_producidas), 0) AS total_pacas,
    ROUND(AVG(dp_total.total_paro_min), 1) AS promedio_minutos_paro,
    ROUND(
        100 - AVG(dp_total.total_paro_min / NULLIF(rp.horas_trabajadas * 60, 0)) * 100
    , 1) AS productividad_promedio
FROM registro_produccion rp
INNER JOIN turno t ON rp.id_turno = t.id_turno
LEFT JOIN (
    SELECT id_registro, SUM(duracion_minutos) AS total_paro_min
    FROM detalle_paro
    GROUP BY id_registro
) dp_total ON rp.id_registro = dp_total.id_registro
WHERE rp.horas_trabajadas > 0
  AND t.nombre != 'No aplica'
GROUP BY t.nombre
ORDER BY productividad_promedio DESC;


-- ============================================================================
-- CONSULTA 5: MÁQUINAS CON MAYOR TIEMPO ACUMULADO DE PARO
-- ============================================================================
-- Pregunta: ¿Cuál máquina tiene más tiempo perdido por paros?
-- Requisitos SQL demostrados: INNER JOIN, SUM, GROUP BY
-- ============================================================================

SELECT 
    m.nombre AS maquina,
    ROUND(SUM(dp.duracion_minutos), 1) AS total_minutos_paro,
    ROUND(SUM(dp.duracion_minutos) / 60, 1) AS total_horas_paro,
    COUNT(DISTINCT rp.id_registro) AS registros_con_paro
FROM detalle_paro dp
INNER JOIN registro_produccion rp ON dp.id_registro = rp.id_registro
INNER JOIN maquina m ON rp.id_maquina = m.id_maquina
WHERE dp.duracion_minutos > 0
GROUP BY m.nombre
ORDER BY total_minutos_paro DESC;


-- ============================================================================
-- CONSULTA 6: EVOLUCIÓN MENSUAL DE TIEMPOS DE PARO
-- ============================================================================
-- Pregunta: ¿Cómo han evolucionado los paros mes a mes?
-- Requisitos SQL demostrados: JOIN, SUM, GROUP BY, BETWEEN
-- ============================================================================

SELECT 
    YEAR(rp.fecha) AS anio,
    MONTH(rp.fecha) AS mes,
    ROUND(SUM(dp.duracion_minutos) / 60, 1) AS horas_paro_total,
    COUNT(DISTINCT rp.id_registro) AS registros_con_paro,
    ROUND(SUM(dp.duracion_minutos) / COUNT(DISTINCT rp.id_registro), 1) 
        AS promedio_minutos_por_registro
FROM detalle_paro dp
INNER JOIN registro_produccion rp ON dp.id_registro = rp.id_registro
WHERE dp.duracion_minutos > 0
  AND rp.fecha BETWEEN '2023-01-01' AND '2025-12-31'
GROUP BY YEAR(rp.fecha), MONTH(rp.fecha)
ORDER BY anio, mes;


-- ============================================================================
-- CONSULTA 7: CAUSAS DE PARO MÁS FRECUENTES (TOP 10)
-- ============================================================================
-- Pregunta: ¿Cuáles son los paros que ocurren con más frecuencia?
-- Requisitos SQL demostrados: INNER JOIN, COUNT, GROUP BY, HAVING
-- ============================================================================

SELECT 
    cp.numero AS codigo,
    cp.descripcion,
    COUNT(*) AS veces_ocurrido,
    ROUND(SUM(dp.duracion_minutos) / 60, 1) AS total_horas,
    ROUND(AVG(dp.duracion_minutos), 1) AS duracion_promedio_minutos
FROM detalle_paro dp
INNER JOIN codigo_paro cp ON dp.id_codigo = cp.id_codigo
WHERE dp.duracion_minutos > 0
GROUP BY cp.numero, cp.descripcion
HAVING COUNT(*) >= 10
ORDER BY veces_ocurrido DESC
LIMIT 10;




-- ============================================================================
-- CONSULTA 8: DISTRIBUCIÓN DE PAROS POR ÁREA DE IMPACTO
-- ============================================================================
-- Pregunta: ¿Qué área genera más tiempo de paro?
-- Requisitos SQL demostrados: INNER JOIN, SUM, GROUP BY
-- ============================================================================

SELECT 
    cp.area_impacto,
    COUNT(*) AS cantidad_paros,
    ROUND(SUM(dp.duracion_minutos) / 60, 1) AS total_horas,
    ROUND(
        SUM(dp.duracion_minutos) / (
            SELECT SUM(duracion_minutos) FROM detalle_paro WHERE duracion_minutos > 0
        ) * 100
    , 1) AS porcentaje_total
FROM detalle_paro dp
INNER JOIN codigo_paro cp ON dp.id_codigo = cp.id_codigo
WHERE dp.duracion_minutos > 0
GROUP BY cp.area_impacto
ORDER BY total_horas DESC;


-- ============================================================================
-- CONSULTA 9: OPERARIOS CON REGISTROS SIN PRODUCCIÓN
-- ============================================================================
-- Pregunta: ¿Cuántos turnos tuvo cada operario sin producción reportada?
-- Requisitos SQL demostrados: LEFT JOIN, COUNT, GROUP BY, HAVING
-- ============================================================================

SELECT 
    o.pseudonimo AS operario,
    COUNT(*) AS total_registros,
    SUM(CASE WHEN rp.pacas_producidas IS NULL OR rp.pacas_producidas = 0 THEN 1 ELSE 0 END) 
        AS registros_sin_produccion,
    ROUND(
        SUM(CASE WHEN rp.pacas_producidas IS NULL OR rp.pacas_producidas = 0 THEN 1 ELSE 0 END) 
        / COUNT(*) * 100
    , 1) AS porcentaje_sin_produccion
FROM registro_produccion rp
LEFT JOIN operario o ON rp.id_operario = o.id_operario
WHERE o.pseudonimo IS NOT NULL
GROUP BY o.pseudonimo
HAVING COUNT(*) >= 10
ORDER BY porcentaje_sin_produccion DESC;



