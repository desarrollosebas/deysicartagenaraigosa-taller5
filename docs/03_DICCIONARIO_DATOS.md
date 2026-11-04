# 03 — Diccionario de Datos

> Motor: **MySQL 8.x** | Esquema: `paros_produccion`

---

## Tabla: `maquina`
**Descripción**: Catálogo de las 4 líneas de envasado de vinilos y témperas.

| Campo | Tipo | Nulo | Default | Restricciones | Descripción |
|-------|------|------|---------|---------------|-------------|
| id_maquina | SMALLINT UNSIGNED | NO | AUTO_INCREMENT | PK | Identificador único |
| nombre | VARCHAR(30) | NO | — | UNIQUE, NOT NULL | Nombre de la línea (ej. Vinilos_1) |
| factor_produccion | DECIMAL(4,2) | NO | 1.00 | CHECK(factor_produccion > 0) | Factor de ajuste de eficiencia |
| activa | BOOLEAN | NO | TRUE | — | Si la línea está en operación |

**Justificación de restricciones**:
- `UNIQUE(nombre)`: No pueden existir dos máquinas con el mismo nombre (RN-001)
- `CHECK(factor_produccion > 0)`: El factor debe ser positivo (RN-002)
- `DEFAULT TRUE`: Las máquinas se asumen activas al crearlas

---

## Tabla: `turno`
**Descripción**: Catálogo de turnos de trabajo disponibles.

| Campo | Tipo | Nulo | Default | Restricciones | Descripción |
|-------|------|------|---------|---------------|-------------|
| id_turno | SMALLINT UNSIGNED | NO | AUTO_INCREMENT | PK | Identificador único |
| nombre | VARCHAR(30) | NO | — | UNIQUE, NOT NULL | Nombre descriptivo del turno |
| hora_inicio | TIME | SÍ | NULL | — | Hora de inicio |
| hora_fin | TIME | SÍ | NULL | — | Hora de fin |
| duracion_horas | DECIMAL(4,1) | SÍ | NULL | CHECK(duracion_horas > 0) | Horas del turno |
| minutos_alimentacion | SMALLINT UNSIGNED | NO | 40 | — | Minutos de alimentación/aseo asignados |
| minutos_pausa | SMALLINT UNSIGNED | NO | 3 | — | Minutos de pausa activa asignados |

**Justificación**:
- `hora_inicio`/`hora_fin` permiten NULL para el turno "No aplica" (RN-006)
- `minutos_alimentacion`/`minutos_pausa`: Los códigos 16 y 17 se asignan automáticamente (RN-025)

---

## Tabla: `operario`
**Descripción**: Personal de producción. Nombres pseudonimizados para proteger datos personales.

| Campo | Tipo | Nulo | Default | Restricciones | Descripción |
|-------|------|------|---------|---------------|-------------|
| id_operario | SMALLINT UNSIGNED | NO | AUTO_INCREMENT | PK | Identificador único |
| pseudonimo | VARCHAR(10) | NO | — | UNIQUE, NOT NULL | Identificador anónimo (ej. OP-001) |
| activo | BOOLEAN | NO | TRUE | — | Si el operario está activo |

**Justificación**: Pseudonimización para repositorio público (RN-011)

---

## Tabla: `referencia`
**Descripción**: Catálogo de productos (referencias de vinilos y témperas).

| Campo | Tipo | Nulo | Default | Restricciones | Descripción |
|-------|------|------|---------|---------------|-------------|
| id_referencia | SMALLINT UNSIGNED | NO | AUTO_INCREMENT | PK | Identificador único |
| nombre | VARCHAR(80) | NO | — | UNIQUE, NOT NULL | Nombre del producto |

---

## Tabla: `referencia_maquina`
**Descripción**: Relación entre productos y máquinas con sus métricas de producción.

| Campo | Tipo | Nulo | Default | Restricciones | Descripción |
|-------|------|------|---------|---------------|-------------|
| id_ref_maq | INT UNSIGNED | NO | AUTO_INCREMENT | PK | Identificador único |
| id_referencia | SMALLINT UNSIGNED | NO | — | FK → referencia | Producto |
| id_maquina | SMALLINT UNSIGNED | NO | — | FK → maquina | Línea de envasado |
| unidades_por_minuto | DECIMAL(8,2) | SÍ | NULL | — | Velocidad de producción |
| unidades_por_display | SMALLINT UNSIGNED | SÍ | NULL | — | Unidades por display |
| displays_por_paca | SMALLINT UNSIGNED | SÍ | NULL | — | Displays por paca |

| Restricción | Tipo | Detalle |
|------------|------|---------|
| UNIQUE(id_referencia, id_maquina) | UNIQUE | Una referencia se registra una sola vez por máquina |
| FK id_referencia | ON DELETE RESTRICT, ON UPDATE CASCADE | No permitir borrar una referencia con datos asociados |
| FK id_maquina | ON DELETE RESTRICT, ON UPDATE CASCADE | No permitir borrar una máquina con datos asociados |

---

## Tabla: `codigo_paro`
**Descripción**: Catálogo de los 18 códigos de paro de producción.

| Campo | Tipo | Nulo | Default | Restricciones | Descripción |
|-------|------|------|---------|---------------|-------------|
| id_codigo | SMALLINT UNSIGNED | NO | AUTO_INCREMENT | PK | Identificador único |
| numero | TINYINT UNSIGNED | NO | — | UNIQUE, CHECK(numero BETWEEN 1 AND 18) | Número del código (01-18) |
| descripcion | VARCHAR(100) | NO | — | NOT NULL | Descripción del paro |
| area_impacto | VARCHAR(40) | NO | — | NOT NULL | Área responsable |
| tiene_subcodigos | BOOLEAN | NO | FALSE | — | Si este código tiene subcódigos |

---

## Tabla: `subcodigo_paro`
**Descripción**: Subcódigos que detallan la causa de un paro (solo para códigos 01, 03, 05).

| Campo | Tipo | Nulo | Default | Restricciones | Descripción |
|-------|------|------|---------|---------------|-------------|
| id_subcodigo | SMALLINT UNSIGNED | NO | AUTO_INCREMENT | PK | Identificador único |
| id_codigo_padre | SMALLINT UNSIGNED | NO | — | FK → codigo_paro | Código padre (01, 03 o 05) |
| codigo | VARCHAR(10) | NO | — | NOT NULL | Código alfanumérico (ej. 1.2.C) |
| descripcion | VARCHAR(100) | NO | — | NOT NULL | Descripción del subcódigo |

| Restricción | Tipo | Detalle |
|------------|------|---------|
| UNIQUE(id_codigo_padre, codigo) | UNIQUE | No duplicar subcódigos dentro de un código padre |
| FK id_codigo_padre | ON DELETE RESTRICT, ON UPDATE CASCADE | El código padre debe existir |

---

## Tabla: `tipo_paro`
**Descripción**: Catálogo de tipos de paro descriptivos (nivel turno/día).

| Campo | Tipo | Nulo | Default | Restricciones | Descripción |
|-------|------|------|---------|---------------|-------------|
| id_tipo_paro | SMALLINT UNSIGNED | NO | AUTO_INCREMENT | PK | Identificador único |
| codigo | VARCHAR(5) | SÍ | NULL | — | Código numérico si existe |
| descripcion | VARCHAR(100) | NO | — | UNIQUE, NOT NULL | Descripción del tipo de paro |

---

## Tabla: `registro_produccion`
**Descripción**: Registro diario de producción por máquina, turno y operario. Tabla principal de hechos.

| Campo | Tipo | Nulo | Default | Restricciones | Descripción |
|-------|------|------|---------|---------------|-------------|
| id_registro | INT UNSIGNED | NO | AUTO_INCREMENT | PK | Identificador único |
| fecha | DATE | NO | — | NOT NULL | Fecha del registro |
| id_maquina | SMALLINT UNSIGNED | NO | — | FK → maquina | Línea de envasado |
| id_turno | SMALLINT UNSIGNED | NO | — | FK → turno | Turno de trabajo |
| id_operario | SMALLINT UNSIGNED | SÍ | NULL | FK → operario | Operario (NULL si "No aplica") |
| id_referencia | SMALLINT UNSIGNED | SÍ | NULL | FK → referencia | Producto fabricado |
| horas_trabajadas | DECIMAL(4,1) | SÍ | NULL | CHECK(horas_trabajadas >= 0) | Horas efectivas de trabajo |
| meta_por_hora | DECIMAL(8,2) | SÍ | NULL | CHECK(meta_por_hora >= 0) | Pacas objetivo por hora |
| pacas_producidas | INT UNSIGNED | SÍ | NULL | — | Unidades producidas (pacas) |
| horas_no_trabajadas | DECIMAL(4,1) | SÍ | NULL | CHECK(horas_no_trabajadas >= 0) | Horas sin actividad |
| id_tipo_paro | SMALLINT UNSIGNED | SÍ | NULL | FK → tipo_paro | Tipo de paro del turno |
| observaciones_paro | TEXT | SÍ | NULL | — | Descripción del paro |
| tiempo_paro_minutos | DECIMAL(8,2) | SÍ | NULL | CHECK(tiempo_paro_minutos >= 0) | Tiempo total de paro en minutos |
| observaciones | TEXT | SÍ | NULL | — | Observaciones generales |

| Restricción | Tipo | Detalle |
|------------|------|---------|
| FK id_maquina | ON DELETE RESTRICT, ON UPDATE CASCADE | No borrar máquina con registros |
| FK id_turno | ON DELETE RESTRICT, ON UPDATE CASCADE | No borrar turno con registros |
| FK id_operario | ON DELETE SET NULL, ON UPDATE CASCADE | Si se elimina operario, se conserva el registro |
| FK id_referencia | ON DELETE SET NULL, ON UPDATE CASCADE | Si se elimina referencia, se conserva el registro |
| FK id_tipo_paro | ON DELETE SET NULL, ON UPDATE CASCADE | Preservar registros si cambia catálogo |

**Justificación de ON DELETE**:
- RESTRICT en máquina y turno: Son datos estructurales, nunca deben borrarse con datos asociados
- SET NULL en operario: Un operario podría retirarse pero sus registros históricos deben conservarse
- SET NULL en referencia: Un producto podría descontinuarse

---

## Tabla: `detalle_paro`
**Descripción**: Desglose de paros por código dentro de un registro de producción.

| Campo | Tipo | Nulo | Default | Restricciones | Descripción |
|-------|------|------|---------|---------------|-------------|
| id_registro | INT UNSIGNED | NO | — | FK → registro_produccion, PK compuesta | Registro padre |
| id_codigo | SMALLINT UNSIGNED | NO | — | FK → codigo_paro, PK compuesta | Código de paro |
| duracion_minutos | DECIMAL(8,2) | NO | 0 | CHECK(duracion_minutos >= 0) | Duración en minutos |

| Restricción | Tipo | Detalle |
|------------|------|---------|
| PK(id_registro, id_codigo) | PRIMARY KEY | Un código por registro |
| FK id_registro | ON DELETE CASCADE, ON UPDATE CASCADE | Al borrar registro, se borran sus detalles |
| FK id_codigo | ON DELETE RESTRICT, ON UPDATE CASCADE | No borrar un código que tiene datos |

---

## Tabla: `detalle_subcodigo`
**Descripción**: Desglose de subcódigos (solo para códigos 01, 03, 05).

| Campo | Tipo | Nulo | Default | Restricciones | Descripción |
|-------|------|------|---------|---------------|-------------|
| id_detalle_sub | INT UNSIGNED | NO | AUTO_INCREMENT | PK | Identificador único |
| id_registro | INT UNSIGNED | NO | — | FK → registro_produccion | Registro padre |
| id_subcodigo | SMALLINT UNSIGNED | NO | — | FK → subcodigo_paro | Subcódigo de paro |
| duracion_minutos | DECIMAL(8,2) | NO | 0 | CHECK(duracion_minutos >= 0) | Duración en minutos |
| area_involucrada | VARCHAR(30) | SÍ | NULL | — | Área (Operarios / Personal_de_mantenimiento) |
| personal_involucrado | VARCHAR(10) | SÍ | NULL | — | Pseudónimo del personal involucrado |

| Restricción | Tipo | Detalle |
|------------|------|---------|
| FK id_registro | ON DELETE CASCADE, ON UPDATE CASCADE | Cascada al borrar registro |
| FK id_subcodigo | ON DELETE RESTRICT, ON UPDATE CASCADE | Proteger catálogo |

