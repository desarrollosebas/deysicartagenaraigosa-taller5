-- ============================================================================
-- 02_datos_catalogos.sql
-- Carga los catálogos base: máquinas, turnos, códigos, subcódigos, tipos de paro
-- Ejecutar después de: 01_crear_tablas.sql
-- Motor: MySQL 8.x
-- ============================================================================

USE paros_produccion;

-- --------------------------------------------------------
-- Catálogo de máquinas (RN-001, RN-002)
-- --------------------------------------------------------
INSERT INTO maquina (nombre, factor_produccion) VALUES
('Vinilos_1', 1.10),
('Vinilos_2', 1.16),
('Vinilos_3', 1.00),
('Vinilos_4', 1.00);

-- --------------------------------------------------------
-- Catálogo de turnos (RN-004, RN-005, RN-006, RN-025)
-- --------------------------------------------------------
INSERT INTO turno (nombre, hora_inicio, hora_fin, duracion_horas, minutos_alimentacion, minutos_pausa) VALUES
('6am-2pm (Turno 1)',  '06:00:00', '14:00:00', 8.0, 40, 3),
('2pm-10pm (Turno 2)', '14:00:00', '22:00:00', 8.0, 40, 3),
('10pm-6am (Turno 3)', '22:00:00', '06:00:00', 8.0, 40, 3),
('6am-4:30pm',         '06:00:00', '16:30:00', 10.5, 70, 6),
('6am-6pm',            '06:00:00', '18:00:00', 12.0, 70, 6),
('6pm-6am',            '18:00:00', '06:00:00', 12.0, 70, 6),
('No aplica',          NULL,       NULL,        NULL, 0,  0);

-- --------------------------------------------------------
-- Catálogo de 18 códigos de paro (RN-023)
-- Fuente: TABLA CODIGOS del Excel + formulario del PDF
-- --------------------------------------------------------
INSERT INTO codigo_paro (numero, descripcion, area_impacto, tiene_subcodigos) VALUES
( 1, 'Falla del sistema electromecánico y/o de control',                'Mantenimiento',           TRUE),
( 2, 'Espera de soporte de mantenimiento',                              'Mantenimiento',           FALSE),
( 3, 'Novedad en los sistemas de potencia (Aire, energía, vapor)',      'Mantenimiento',           TRUE),
( 4, 'Mantenimiento preventivo',                                        'Mantenimiento',           FALSE),
( 5, 'Ajuste operativo',                                                'Producción',              TRUE),
( 6, 'Limpieza por derrame operativo',                                  'Producción',              FALSE),
( 7, 'Alistamiento de máquina / Cambio de referencia',                  'Producción',              FALSE),
( 8, 'Capacitación / Reunión',                                          'Producción',              FALSE),
( 9, 'Falta de operario',                                               'Producción',              FALSE),
(10, 'Paro por ventaja/evacuación',                                     'Producción',              FALSE),
(11, 'Reproceso',                                                       'Producción',              FALSE),
(12, 'Materia prima defectuosa',                                        'Calidad',                 FALSE),
(13, 'En espera por el aval del laboratorio de microbiología',          'Calidad',                 FALSE),
(14, 'Falta de materia prima',                                          'Almacén de materias primas', FALSE),
(15, 'Cambio de insumos (Roscadores, O''ring, Etiquetas)',              'Paro programado',         FALSE),
(16, 'Alimentación y aseo de la zona de trabajo y la máquina',          'Paro programado',         FALSE),
(17, 'Pausa activa',                                                    'Paro programado',         FALSE),
(18, 'Desinfección',                                                    'Paro programado',         FALSE);

-- --------------------------------------------------------
-- Subcódigos del código 01: Falla del sistema electromecánico
-- Fuente: TABLA CODIGOS del Excel (columna H)
-- --------------------------------------------------------
INSERT INTO subcodigo_paro (id_codigo_padre, codigo, descripcion) VALUES
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.1',   'Sistema alimentador de envases'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.1.A', 'Banda'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.1.B', 'Motor'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.1.C', 'Sensor'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.2',   'Sistema de dosificación'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.2.A', 'Cambio de racores'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.2.B', 'Ajuste de sensor'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.2.C', 'Cambio de válvula'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.2.D', 'Retenedores'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.2.E', 'O''Ring'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.3',   'Sistema de banda de entrada'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.3.A', 'Banda'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.3.B', 'Motor'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.4',   'Sistema de tapado'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.4.A', 'Motor del transfer'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.4.B', 'Pisador de tapa'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.4.3', 'Sensor'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.5',   'Sistema de alimentación de tapa'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.5.A', 'Banda'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.5.B', 'Motor'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.5.C', 'Sensor'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.6',   'Sistema Video Jet'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.6.A', 'Fotocelda'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.6.B', 'Sensor'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.7',   'Sistema de sujeción y roscadores'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.7.A', 'Banda de sujeción'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.7.B', 'Roscadores'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.8',   'Sistema etiquetadora'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.8.A', 'Banda'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.8.B', 'Motor'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 1), '1.8.C', 'Sensor');

-- --------------------------------------------------------
-- Subcódigos del código 03: Novedad en sistemas de potencia
-- --------------------------------------------------------
INSERT INTO subcodigo_paro (id_codigo_padre, codigo, descripcion) VALUES
((SELECT id_codigo FROM codigo_paro WHERE numero = 3), '3.1', 'Fallo en la subestación'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 3), '3.2', 'Fallo en la red pública'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 3), '3.3', 'Falla en la red neumática o el compresor'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 3), '3.4', 'Falla en la red de enfriamiento o el chiller'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 3), '3.5', 'Falla en la red de vapor o la caldera');

-- --------------------------------------------------------
-- Subcódigos del código 05: Ajuste operativo
-- --------------------------------------------------------
INSERT INTO subcodigo_paro (id_codigo_padre, codigo, descripcion) VALUES
((SELECT id_codigo FROM codigo_paro WHERE numero = 5), '5.1',  'Sistema alimentador de envases'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 5), '5.2',  'Sistema de dosificación de pintura, frontal posterior'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 5), '5.3',  'Banda transportadora de entrada'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 5), '5.4',  'Banda transportadora de salida'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 5), '5.5',  'Transfer y pisador de tapa'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 5), '5.6',  'Sistema alimentador de tapa y tobogán'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 5), '5.7',  'Video Jet'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 5), '5.8',  'Banda de sujeción y roscadores'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 5), '5.9',  'Sistema de etiquetado'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 5), '5.10', 'Purga de color'),
((SELECT id_codigo FROM codigo_paro WHERE numero = 5), '5.11', 'Lavado de boquilla');

-- --------------------------------------------------------
-- Catálogo de tipos de paro (RN-031 a RN-034)
-- ORDEN ALINEADO con la migración (los IDs auto_increment
-- deben coincidir con los id_tipo_paro en 06_datos_registros.sql)
-- --------------------------------------------------------
INSERT INTO tipo_paro (codigo, descripcion) VALUES
('19', 'No aplica'),                                                         -- ID 1
('14', 'Falta de materia prima'),                                            -- ID 2
('05', 'Ajuste operativo'),                                                  -- ID 3
('09', 'Falta de operario'),                                                 -- ID 4
('18', 'Paro de máquina por ventas'),                                        -- ID 5
('13', 'En espera por el aval del laboratorio de microbiología'),             -- ID 6
('07', 'Alistamiento de máquina / Cambio de referencia'),                     -- ID 7
('03', 'Novedad en los sistemas de potencia (Aire, energía, vapor)'),         -- ID 8
('12', 'Materia prima defectuosa o material de empaque no conforme'),         -- ID 9
('17', 'Paro de máquina'),                                                   -- ID 10
('6',  'Falta de materiales o materias primas'),                              -- ID 11
('5',  'Aislamiento/cambio de producto'),                                     -- ID 12
('15', 'Aprobación de laboratorio (microbiología)'),                          -- ID 13
('10', 'Paro por materia prima o material de empaque no conforme'),           -- ID 14
('11', 'Limpieza no programada'),                                             -- ID 15
('16', 'Paro por proceso anterior'),                                          -- ID 16
('9',  'Falta de programación (planeación)'),                                 -- ID 17
('3',  'Ajuste eléctrico o de servicios (aire, caldera, gas)'),               -- ID 18
('4',  'Ajuste de operación');                                                -- ID 19

