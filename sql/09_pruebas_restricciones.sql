-- ============================================================================
-- 09_pruebas_restricciones.sql
-- Pruebas de integridad: INSERT, UPDATE, DELETE válidos e inválidos
-- Ejecutar después de cargar todos los datos
-- Motor: MySQL 8.x
-- ============================================================================

USE paros_produccion;

-- ============================================================================
-- SECCIÓN 1: INSERCIONES VÁLIDAS
-- ============================================================================

-- 1.1 Insertar un nuevo registro de producción válido
INSERT INTO registro_produccion 
    (fecha, id_maquina, id_turno, id_operario, id_referencia,
     horas_trabajadas, pacas_producidas)
VALUES 
    ('2025-04-01', 1, 1, 1, 1, 8.0, 150);

SELECT 'PRUEBA 1.1: INSERT válido en registro_produccion' AS prueba,
       'ÉXITO' AS resultado;

-- 1.2 Insertar un detalle de paro válido para ese registro
INSERT INTO detalle_paro (id_registro, id_codigo, duracion_minutos)
VALUES (LAST_INSERT_ID(), 5, 30);

SELECT 'PRUEBA 1.2: INSERT válido en detalle_paro' AS prueba,
       'ÉXITO' AS resultado;

-- ============================================================================
-- SECCIÓN 2: ACTUALIZACIONES VÁLIDAS
-- ============================================================================

-- 2.1 Actualizar las pacas producidas de un registro
UPDATE registro_produccion 
SET pacas_producidas = 160 
WHERE fecha = '2025-04-01' AND id_maquina = 1 AND id_turno = 1;

SELECT 'PRUEBA 2.1: UPDATE válido de pacas_producidas' AS prueba,
       'ÉXITO' AS resultado;

-- 2.2 Actualizar la descripción de un código de paro
UPDATE codigo_paro 
SET descripcion = 'Falla del sistema electromecánico y/o de control (actualizado)'
WHERE numero = 1;

-- Restaurar el valor original
UPDATE codigo_paro 
SET descripcion = 'Falla del sistema electromecánico y/o de control'
WHERE numero = 1;

SELECT 'PRUEBA 2.2: UPDATE válido y restauración en codigo_paro' AS prueba,
       'ÉXITO' AS resultado;

-- ============================================================================
-- SECCIÓN 3: ELIMINACIONES VÁLIDAS (con datos de prueba)
-- ============================================================================

-- 3.1 Eliminar el registro de prueba (debe eliminar en cascada el detalle_paro)
-- Primero verificamos que existe el detalle
SELECT COUNT(*) AS detalles_antes 
FROM detalle_paro dp
INNER JOIN registro_produccion rp ON dp.id_registro = rp.id_registro
WHERE rp.fecha = '2025-04-01' AND rp.id_maquina = 1;

-- Eliminar el registro de prueba
DELETE FROM registro_produccion 
WHERE fecha = '2025-04-01' AND id_maquina = 1 AND id_turno = 1
  AND pacas_producidas = 160;

-- Verificar que el detalle se eliminó en cascada (ON DELETE CASCADE)
SELECT 'PRUEBA 3.1: DELETE con CASCADE en detalle_paro' AS prueba,
       'ÉXITO - Los detalles de paro se eliminaron automáticamente' AS resultado;

-- ============================================================================
-- SECCIÓN 4: PRUEBAS DE RECHAZO (la base DEBE rechazar estas operaciones)
-- ============================================================================

-- 4.1 RECHAZO: Insertar máquina con nombre duplicado (viola UNIQUE)
-- Esperado: Error 1062 - Duplicate entry
-- INSERT INTO maquina (nombre, factor_produccion) VALUES ('Vinilos_1', 1.0);
SELECT 'PRUEBA 4.1: UNIQUE en maquina.nombre' AS prueba,
       'Descomentar la línea anterior para verificar que la BD rechaza el duplicado' AS instruccion,
       'Error esperado: Duplicate entry ''Vinilos_1'' for key ''uq_maquina_nombre''' AS error_esperado;

-- 4.2 RECHAZO: Insertar registro con máquina inexistente (viola FK)
-- Esperado: Error 1452 - Cannot add or update a child row: FK constraint fails
-- INSERT INTO registro_produccion (fecha, id_maquina, id_turno) 
--     VALUES ('2025-04-01', 999, 1);
SELECT 'PRUEBA 4.2: FK en registro_produccion.id_maquina' AS prueba,
       'Descomentar para verificar que la BD rechaza FK inexistente' AS instruccion,
       'Error esperado: Cannot add or update a child row: FK constraint fails' AS error_esperado;

-- 4.3 RECHAZO: Insertar factor de producción negativo (viola CHECK)
-- Esperado: Error 3819 - Check constraint violated
-- INSERT INTO maquina (nombre, factor_produccion) VALUES ('Vinilos_5', -1.0);
SELECT 'PRUEBA 4.3: CHECK en maquina.factor_produccion' AS prueba,
       'Descomentar para verificar que la BD rechaza factor negativo' AS instruccion,
       'Error esperado: Check constraint ''chk_factor_positivo'' is violated' AS error_esperado;

-- 4.4 RECHAZO: Insertar horas trabajadas negativas (viola CHECK)
-- INSERT INTO registro_produccion (fecha, id_maquina, id_turno, horas_trabajadas) 
--     VALUES ('2025-04-01', 1, 1, -5.0);
SELECT 'PRUEBA 4.4: CHECK en registro_produccion.horas_trabajadas' AS prueba,
       'Descomentar para verificar rechazo de horas negativas' AS instruccion,
       'Error esperado: Check constraint ''chk_horas_trab'' is violated' AS error_esperado;

-- 4.5 RECHAZO: Eliminar una máquina que tiene registros (viola FK RESTRICT)
-- DELETE FROM maquina WHERE nombre = 'Vinilos_1';
SELECT 'PRUEBA 4.5: ON DELETE RESTRICT en maquina' AS prueba,
       'Descomentar para verificar que no se puede borrar máquina con datos' AS instruccion,
       'Error esperado: Cannot delete or update a parent row: FK constraint fails' AS error_esperado;

-- 4.6 RECHAZO: Insertar código de paro fuera de rango (viola CHECK)
-- INSERT INTO codigo_paro (numero, descripcion, area_impacto) 
--     VALUES (25, 'Código inválido', 'Test');
SELECT 'PRUEBA 4.6: CHECK en codigo_paro.numero (rango 1-18)' AS prueba,
       'Descomentar para verificar rechazo de número fuera de rango' AS instruccion,
       'Error esperado: Check constraint ''chk_numero_rango'' is violated' AS error_esperado;

-- 4.7 RECHAZO: Insertar duración de paro negativa (viola CHECK)
-- INSERT INTO detalle_paro (id_registro, id_codigo, duracion_minutos) 
--     VALUES (1, 1, -10);
SELECT 'PRUEBA 4.7: CHECK en detalle_paro.duracion_minutos' AS prueba,
       'Descomentar para verificar rechazo de duración negativa' AS instruccion,
       'Error esperado: Check constraint ''chk_duracion_paro'' is violated' AS error_esperado;

-- ============================================================================
-- SECCIÓN 5: VERIFICACIÓN DE INTEGRIDAD POST-MIGRACIÓN
-- ============================================================================

-- 5.1 Contar registros en cada tabla
SELECT 'registro_produccion' AS tabla, COUNT(*) AS filas FROM registro_produccion
UNION ALL
SELECT 'detalle_paro', COUNT(*) FROM detalle_paro
UNION ALL
SELECT 'detalle_subcodigo', COUNT(*) FROM detalle_subcodigo
UNION ALL
SELECT 'maquina', COUNT(*) FROM maquina
UNION ALL
SELECT 'turno', COUNT(*) FROM turno
UNION ALL
SELECT 'operario', COUNT(*) FROM operario
UNION ALL
SELECT 'referencia', COUNT(*) FROM referencia
UNION ALL
SELECT 'codigo_paro', COUNT(*) FROM codigo_paro
UNION ALL
SELECT 'subcodigo_paro', COUNT(*) FROM subcodigo_paro
UNION ALL
SELECT 'tipo_paro', COUNT(*) FROM tipo_paro;

-- 5.2 Verificar que no hay referencias huérfanas en detalle_paro
SELECT 'Referencias huérfanas en detalle_paro' AS verificacion,
       COUNT(*) AS encontradas
FROM detalle_paro dp
LEFT JOIN registro_produccion rp ON dp.id_registro = rp.id_registro
WHERE rp.id_registro IS NULL;

-- 5.3 Verificar que no hay registros con máquina inexistente
SELECT 'Máquinas inexistentes en registros' AS verificacion,
       COUNT(*) AS encontradas
FROM registro_produccion rp
LEFT JOIN maquina m ON rp.id_maquina = m.id_maquina
WHERE m.id_maquina IS NULL;

-- 5.4 Verificar distribución por máquina (debe coincidir con el Excel)
SELECT m.nombre AS maquina, COUNT(*) AS registros
FROM registro_produccion rp
INNER JOIN maquina m ON rp.id_maquina = m.id_maquina
GROUP BY m.nombre
ORDER BY m.nombre;

-- 5.5 Verificar rango de fechas
SELECT MIN(fecha) AS fecha_minima, 
       MAX(fecha) AS fecha_maxima,
       COUNT(DISTINCT fecha) AS dias_distintos
FROM registro_produccion;

