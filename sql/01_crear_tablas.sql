-- ============================================================================
-- 01_crear_tablas.sql
-- Crea todas las tablas del esquema normalizado
-- Ejecutar después de: 00_crear_base_datos.sql
-- Motor: MySQL 8.x
-- ============================================================================

USE paros_produccion;

-- --------------------------------------------------------
-- Tabla: maquina
-- Catálogo de las 4 líneas de envasado
-- Reglas de negocio: RN-001, RN-002, RN-003
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS maquina (
    id_maquina   SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre       VARCHAR(30)       NOT NULL,
    factor_produccion DECIMAL(4,2) NOT NULL DEFAULT 1.00,
    activa       BOOLEAN           NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id_maquina),
    CONSTRAINT uq_maquina_nombre UNIQUE (nombre),
    CONSTRAINT chk_factor_positivo CHECK (factor_produccion > 0)
) ENGINE=InnoDB COMMENT='Catálogo de líneas de envasado (Vinilos_1 a Vinilos_4)';

-- --------------------------------------------------------
-- Tabla: turno
-- Catálogo de turnos de trabajo
-- Reglas de negocio: RN-004, RN-005, RN-006, RN-007, RN-025
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS turno (
    id_turno      SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre        VARCHAR(30)       NOT NULL,
    hora_inicio   TIME              NULL DEFAULT NULL,
    hora_fin      TIME              NULL DEFAULT NULL,
    duracion_horas DECIMAL(4,1)     NULL DEFAULT NULL,
    minutos_alimentacion SMALLINT UNSIGNED NOT NULL DEFAULT 40,
    minutos_pausa SMALLINT UNSIGNED NOT NULL DEFAULT 3,
    PRIMARY KEY (id_turno),
    CONSTRAINT uq_turno_nombre UNIQUE (nombre),
    CONSTRAINT chk_duracion_positiva CHECK (duracion_horas IS NULL OR duracion_horas > 0)
) ENGINE=InnoDB COMMENT='Catálogo de turnos de trabajo';

-- --------------------------------------------------------
-- Tabla: operario
-- Personal de producción (pseudonimizado)
-- Reglas de negocio: RN-008, RN-009, RN-010, RN-011
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS operario (
    id_operario  SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    pseudonimo   VARCHAR(10)       NOT NULL,
    activo       BOOLEAN           NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id_operario),
    CONSTRAINT uq_operario_pseudo UNIQUE (pseudonimo)
) ENGINE=InnoDB COMMENT='Personal de producción (nombres pseudonimizados)';

-- --------------------------------------------------------
-- Tabla: referencia
-- Catálogo de productos (vinilos y témperas)
-- Reglas de negocio: RN-012, RN-013, RN-015
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS referencia (
    id_referencia SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre        VARCHAR(80)       NOT NULL,
    PRIMARY KEY (id_referencia),
    CONSTRAINT uq_referencia_nombre UNIQUE (nombre)
) ENGINE=InnoDB COMMENT='Catálogo de productos fabricados';

-- --------------------------------------------------------
-- Tabla: referencia_maquina
-- Relación N:M entre productos y máquinas con métricas de producción
-- Reglas de negocio: RN-013, RN-014
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS referencia_maquina (
    id_ref_maq       INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    id_referencia    SMALLINT UNSIGNED NOT NULL,
    id_maquina       SMALLINT UNSIGNED NOT NULL,
    unidades_por_minuto DECIMAL(8,2)   NULL DEFAULT NULL,
    unidades_por_display SMALLINT UNSIGNED NULL DEFAULT NULL,
    displays_por_paca    SMALLINT UNSIGNED NULL DEFAULT NULL,
    PRIMARY KEY (id_ref_maq),
    CONSTRAINT uq_ref_maq UNIQUE (id_referencia, id_maquina),
    CONSTRAINT fk_refmaq_referencia FOREIGN KEY (id_referencia)
        REFERENCES referencia(id_referencia)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_refmaq_maquina FOREIGN KEY (id_maquina)
        REFERENCES maquina(id_maquina)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Métricas de producción por combinación producto-máquina';

-- --------------------------------------------------------
-- Tabla: codigo_paro
-- Catálogo de los 18 códigos de paro
-- Reglas de negocio: RN-021, RN-023
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS codigo_paro (
    id_codigo    SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    numero       TINYINT UNSIGNED  NOT NULL,
    descripcion  VARCHAR(100)      NOT NULL,
    area_impacto VARCHAR(40)       NOT NULL,
    tiene_subcodigos BOOLEAN       NOT NULL DEFAULT FALSE,
    PRIMARY KEY (id_codigo),
    CONSTRAINT uq_codigo_numero UNIQUE (numero),
    CONSTRAINT chk_numero_rango CHECK (numero BETWEEN 1 AND 18)
) ENGINE=InnoDB COMMENT='Catálogo de 18 códigos de paro de producción';

-- --------------------------------------------------------
-- Tabla: subcodigo_paro
-- Subcódigos que detallan los códigos 01, 03 y 05
-- Reglas de negocio: RN-026, RN-027, RN-028, RN-029
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS subcodigo_paro (
    id_subcodigo    SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_codigo_padre SMALLINT UNSIGNED NOT NULL,
    codigo          VARCHAR(10)       NOT NULL,
    descripcion     VARCHAR(100)      NOT NULL,
    PRIMARY KEY (id_subcodigo),
    CONSTRAINT uq_subcodigo UNIQUE (id_codigo_padre, codigo),
    CONSTRAINT fk_subcod_codigo FOREIGN KEY (id_codigo_padre)
        REFERENCES codigo_paro(id_codigo)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Subcódigos de paro (solo para códigos 01, 03, 05)';

-- --------------------------------------------------------
-- Tabla: tipo_paro
-- Catálogo de tipos de paro descriptivos
-- Reglas de negocio: RN-031, RN-032, RN-033, RN-034
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS tipo_paro (
    id_tipo_paro SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    codigo       VARCHAR(5)        NULL DEFAULT NULL,
    descripcion  VARCHAR(100)      NOT NULL,
    PRIMARY KEY (id_tipo_paro),
    CONSTRAINT uq_tipo_paro_desc UNIQUE (descripcion)
) ENGINE=InnoDB COMMENT='Catálogo de tipos de paro descriptivos';

-- --------------------------------------------------------
-- Tabla: registro_produccion
-- Tabla principal de hechos: registro diario por máquina/turno
-- Reglas de negocio: RN-016 a RN-020, RN-035, RN-045, RN-046
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS registro_produccion (
    id_registro       INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    fecha             DATE              NOT NULL,
    id_maquina        SMALLINT UNSIGNED NOT NULL,
    id_turno          SMALLINT UNSIGNED NOT NULL,
    id_operario       SMALLINT UNSIGNED NULL DEFAULT NULL,
    id_referencia     SMALLINT UNSIGNED NULL DEFAULT NULL,
    horas_trabajadas  DECIMAL(4,1)      NULL DEFAULT NULL,
    meta_por_hora     DECIMAL(8,2)      NULL DEFAULT NULL,
    pacas_producidas  INT UNSIGNED      NULL DEFAULT NULL,
    horas_no_trabajadas DECIMAL(4,1)    NULL DEFAULT NULL,
    id_tipo_paro      SMALLINT UNSIGNED NULL DEFAULT NULL,
    observaciones_paro TEXT             NULL DEFAULT NULL,
    tiempo_paro_minutos DECIMAL(8,2)    NULL DEFAULT NULL,
    observaciones     TEXT              NULL DEFAULT NULL,
    PRIMARY KEY (id_registro),
    CONSTRAINT fk_reg_maquina FOREIGN KEY (id_maquina)
        REFERENCES maquina(id_maquina)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_reg_turno FOREIGN KEY (id_turno)
        REFERENCES turno(id_turno)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_reg_operario FOREIGN KEY (id_operario)
        REFERENCES operario(id_operario)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_reg_referencia FOREIGN KEY (id_referencia)
        REFERENCES referencia(id_referencia)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_reg_tipo_paro FOREIGN KEY (id_tipo_paro)
        REFERENCES tipo_paro(id_tipo_paro)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT chk_horas_trab CHECK (horas_trabajadas IS NULL OR horas_trabajadas >= 0),
    CONSTRAINT chk_meta CHECK (meta_por_hora IS NULL OR meta_por_hora >= 0),
    CONSTRAINT chk_horas_no_trab CHECK (horas_no_trabajadas IS NULL OR horas_no_trabajadas >= 0),
    CONSTRAINT chk_tiempo_paro CHECK (tiempo_paro_minutos IS NULL OR tiempo_paro_minutos >= 0)
) ENGINE=InnoDB COMMENT='Registros diarios de producción por máquina y turno';

-- --------------------------------------------------------
-- Tabla: detalle_paro
-- Desglose de paros por código dentro de un registro
-- Reglas de negocio: RN-021, RN-022, RN-024
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS detalle_paro (
    id_registro      INT UNSIGNED      NOT NULL,
    id_codigo        SMALLINT UNSIGNED NOT NULL,
    duracion_minutos DECIMAL(8,2)      NOT NULL DEFAULT 0,
    PRIMARY KEY (id_registro, id_codigo),
    CONSTRAINT fk_dp_registro FOREIGN KEY (id_registro)
        REFERENCES registro_produccion(id_registro)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_dp_codigo FOREIGN KEY (id_codigo)
        REFERENCES codigo_paro(id_codigo)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_duracion_paro CHECK (duracion_minutos >= 0)
) ENGINE=InnoDB COMMENT='Desglose de paros por código en cada registro';

-- --------------------------------------------------------
-- Tabla: detalle_subcodigo
-- Desglose detallado de subcódigos (códigos 01, 03, 05)
-- Reglas de negocio: RN-026 a RN-030, RN-047, RN-048
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS detalle_subcodigo (
    id_detalle_sub     INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    id_registro        INT UNSIGNED      NOT NULL,
    id_subcodigo       SMALLINT UNSIGNED NOT NULL,
    duracion_minutos   DECIMAL(8,2)      NOT NULL DEFAULT 0,
    area_involucrada   VARCHAR(30)       NULL DEFAULT NULL,
    personal_involucrado VARCHAR(10)     NULL DEFAULT NULL,
    PRIMARY KEY (id_detalle_sub),
    CONSTRAINT fk_ds_registro FOREIGN KEY (id_registro)
        REFERENCES registro_produccion(id_registro)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_ds_subcodigo FOREIGN KEY (id_subcodigo)
        REFERENCES subcodigo_paro(id_subcodigo)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_duracion_sub CHECK (duracion_minutos >= 0)
) ENGINE=InnoDB COMMENT='Detalle de subcódigos de paro';

