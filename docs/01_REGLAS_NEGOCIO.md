# 01 — Reglas de Negocio

> Documento de la FASE 1 del proyecto.  
> Las reglas se clasifican en: **[H]** = Hecho del insumo, **[I]** = Inferencia razonada, **[D]** = Decisión de diseño propuesta.

---

## Entidades principales

### Líneas de envasado (Máquinas)

| ID | Regla | Tipo |
|----|-------|------|
| RN-001 | La empresa opera **4 líneas de envasado**: Vinilos_1, Vinilos_2, Vinilos_3 y Vinilos_4. | [H] |
| RN-002 | Cada línea de envasado tiene un **factor de producción** particular que ajusta el cálculo de eficiencia: Vinilos_1=1.1, Vinilos_2=1.16, Vinilos_3=1.0, Vinilos_4=1.0. | [H] |
| RN-003 | Una línea de envasado puede producir múltiples referencias (productos). No todas las referencias se fabrican en todas las líneas. | [H] |

### Turnos

| ID | Regla | Tipo |
|----|-------|------|
| RN-004 | Existen **3 turnos estándar**: Turno 1 (6am-2pm), Turno 2 (2pm-10pm), Turno 3 (10pm-6am). | [H] |
| RN-005 | Existen turnos especiales: 6am-4:30pm (jornada extendida diurna), 6am-6pm y 6pm-6am (turnos de 12 horas). | [H] |
| RN-006 | El valor "No aplica" en turno se usa cuando no hubo producción ese día o la máquina estuvo fuera de servicio. | [I] |
| RN-007 | Cada turno tiene un número fijo de horas disponibles para producción. | [I] |

### Operarios

| ID | Regla | Tipo |
|----|-------|------|
| RN-008 | Cada registro de producción se asocia a **una operaria/o** responsable de la línea durante ese turno. | [H] |
| RN-009 | Una misma operaria puede trabajar en diferentes líneas y turnos en distintos días. | [H] |
| RN-010 | El campo operario puede quedar vacío cuando no hay producción ("No aplica"). | [H] |
| RN-011 | Los nombres de operarios son **datos personales protegidos**; deben pseudonimizarse para el repositorio público. | [D] |

### Referencias (Productos)

| ID | Regla | Tipo |
|----|-------|------|
| RN-012 | Una **referencia** es un producto específico (ej. "Parchesitos 22cc (6 col)"). | [H] |
| RN-013 | Cada referencia tiene atributos de conversión: unidades producidas por minuto, unidades por display y displays por paca. Estos valores dependen de la combinación máquina-referencia. | [H] |
| RN-014 | El catálogo de referencias es diferente por máquina (las fórmulas de meta usan XLOOKUP por máquina). | [H] |
| RN-015 | "No aplica" como referencia indica que no hubo producción. | [H] |

### Registro de producción

| ID | Regla | Tipo |
|----|-------|------|
| RN-016 | Un **registro de producción** representa la actividad de **una línea, un turno y un día** específicos. | [H] |
| RN-017 | Un registro contiene: fecha, máquina, turno, operario, referencia, horas trabajadas, meta por hora, pacas producidas, horas sin trabajar. | [H] |
| RN-018 | Las **pacas producidas** son la unidad de medida de producción. | [H] |
| RN-019 | La **meta por hora** es la cantidad esperada de pacas por hora para esa referencia en esa máquina. | [I] |
| RN-020 | Un registro puede no tener pacas producidas (3,051 de 8,208 filas). Esto ocurre cuando el registro corresponde a un día sin producción, un subcódigo o un registro incompleto. | [H] |

### Paros de producción

| ID | Regla | Tipo |
|----|-------|------|
| RN-021 | Cada registro de producción puede tener asociados **paros de producción** en uno o más de los 18 códigos. | [H] |
| RN-022 | La duración de cada paro se registra en **minutos** y se convierte a horas (minutos/60). | [H] |
| RN-023 | Los 18 **códigos de paro** están catalogados con un área de impacto (Mantenimiento, Producción, Calidad, Almacén, Paro programado). | [H] |
| RN-024 | Un registro puede tener paros en múltiples códigos simultáneamente. | [H] |
| RN-025 | Los códigos 16 (Alimentación y aseo) y 17 (Pausa activa) se asignan automáticamente según el turno: Turno estándar = 40 min (cod 16) + 3 min (cod 17); Turno 6am-4:30pm = 70 min + 6 min. | [H] |

### Subcódigos de paro

| ID | Regla | Tipo |
|----|-------|------|
| RN-026 | Solo los códigos **01, 03 y 05** tienen subcódigos que detallan la causa específica del paro. | [H] |
| RN-027 | Los subcódigos del código 01 detallan el sistema mecánico afectado (alimentador, dosificación, banda, tapado, video jet, sujeción, etiquetadora) y su componente específico. | [H] |
| RN-028 | Los subcódigos del código 03 detallan el tipo de falla de potencia (subestación, red pública, neumática, enfriamiento, vapor). | [H] |
| RN-029 | Los subcódigos del código 05 detallan el sistema operativo ajustado, e incluyen información sobre el **área involucrada** (Operarios o Personal_de_mantenimiento) y el **personal involucrado** (nombre). | [H] |
| RN-030 | Un mismo registro de producción puede generar **múltiples filas de subcódigo** (en la tabla de subcódigos). La tabla de subcódigos es una extensión del registro principal. | [H] |

### Tipo de paro (campo descriptivo)

| ID | Regla | Tipo |
|----|-------|------|
| RN-031 | El campo "Tipo de paro" es un **clasificador general** diferente de los códigos numéricos. Describe la razón principal por la que la máquina no produjo al 100%. | [H] |
| RN-032 | "[19] No aplica" significa que **sí hubo producción normal** y los paros son incidentales (alimentación, pausa, ajustes menores). | [I] |
| RN-033 | Valores como "17. PARO DE MAQUINA" y "[18] Paro de máquina por ventas" indican paros mayores donde la máquina no operó durante todo el turno o la mayor parte. | [I] |
| RN-034 | Coexisten dos nomenclaturas históricas: formato antiguo (ej. "17. PARO DE MAQUINA") y formato nuevo con corchetes (ej. "[18] Paro de maquina por ventas"). | [H] |

---

## Indicadores y cálculos

| ID | Regla | Tipo |
|----|-------|------|
| RN-035 | La **eficiencia (productividad)** se calcula como: `IF(producción_real=0, 0, (producción_real / producción_ideal) × fProduccion)` donde producción_ideal = horas_trabajadas × meta_por_hora. | [H] |
| RN-036 | El **porcentaje de cada código de paro** se calcula como la razón entre las horas de ese código y las horas trabajadas totales, por máquina y período. | [I] |
| RN-037 | La **productividad general** por máquina es: `100% − Σ(% de cada código de paro)`. | [I] |
| RN-038 | Los indicadores se generan **mensualmente** y se presentan a la dirección. | [H] |
| RN-039 | Se comparan los indicadores de productividad entre años (ej. 2024 vs 2025) por máquina y por mes. | [H] |

---

## Flujo del proceso

| ID | Regla | Tipo |
|----|-------|------|
| RN-040 | Las operarias diligencian un formato manual "hora a hora" en papel durante el turno. | [H] |
| RN-041 | Los formatos pasan del área de producción al área de mantenimiento. | [H] |
| RN-042 | El personal de mantenimiento transcribe la información al libro Excel. | [H] |
| RN-043 | El Excel genera gráficos e indicadores automáticamente mediante tablas dinámicas. | [H] |
| RN-044 | El coordinador de mantenimiento genera un informe mensual para los jefes de área y la alta dirección. | [H] |

---

## Datos obligatorios y opcionales

| ID | Regla | Tipo |
|----|-------|------|
| RN-045 | Son **obligatorios** en un registro con producción: Fecha, Máquina, Turno, Operario, Referencia, Horas trabajadas. | [I] |
| RN-046 | Son **opcionales**: Pacas producidas (puede ser 0 o vacío si no hubo producción), cada código de paro individual, observaciones. | [I] |
| RN-047 | Los campos de subcódigo son opcionales y solo aplican cuando el código padre (01, 03 o 05) tiene valor > 0. | [H] |
| RN-048 | El campo "Personal involucrado" en subcódigo 5 solo se llena cuando el área involucrada es "Personal_de_mantenimiento". | [I] |

