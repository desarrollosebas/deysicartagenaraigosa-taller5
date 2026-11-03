# 02 — Diagnóstico del Excel y Normalización

---

## 1. Diagnóstico de problemas del Excel

### P-01: Grupos de columnas repetidas (violación de 1FN)

**Evidencia**: La tabla `T_baseDeDatos` tiene 18 pares de columnas `Codigo de paro N` / `Codigo N en horas` (36 columnas).

**Problema**: Los códigos de paro son un **grupo repetitivo**. Cada registro repite la misma estructura 18 veces horizontalmente. Esto:
- Desperdicia espacio (la mayoría de las celdas están en 0)
- Dificulta agregar un código 19 (requiere agregar 2 columnas y modificar fórmulas)
- Impide consultas simples como "¿cuál es el código más frecuente?" sin unir 18 columnas

### P-02: Redundancia de datos calculados

**Evidencia**: El campo `Codigo N en horas` = `Codigo de paro N / 60`. Los campos Mes y Año se derivan de Fecha.

**Problema**: Almacenar valores que se pueden calcular genera:
- Anomalía de actualización: si se corrige el valor en minutos, puede no actualizarse el de horas
- Mayor tamaño de almacenamiento sin necesidad

### P-03: Inconsistencia en catálogos de tipos de paro

**Evidencia**: Coexisten "17. PARO DE MAQUINA", "[18] Paro de maquina por ventas", "9.FALTA DE PROGRAMACIÓN", "[19] No aplica" — formatos heterogéneos.

**Problema**: No hay integridad referencial. El campo es texto libre, no apunta a un catálogo normalizado. Dificulta análisis y genera errores de escritura.

### P-04: Campos multivaluados sin normalizar

**Evidencia**: Un solo registro puede contener subcódigos para los códigos 1, 3 y 5 simultáneamente, pero solo en columnas fijas (no en filas).

**Problema**: Si un registro tuviera dos subcódigos distintos del mismo código padre, la estructura no lo permite. La tabla de subcódigos existe como extensión separada pero no tiene clave foránea formal.

### P-05: Ausencia de integridad referencial

**Evidencia**: Los campos Máquina, Operario, Referencia y Turno son texto libre. No hay tablas maestras con restricciones FK.

**Problema**: Se pueden escribir valores como "Vinilos_5" o un nombre de operario mal escrito sin que el sistema lo rechace.

### P-06: Campos vacíos que dificultan el análisis

**Evidencia**: 3,721 filas sin Operario, 3,912 sin Turno, 3,051 sin Pacas producidas.

**Problema**: No se distingue entre "dato no aplica", "dato no capturado" y "valor real = 0".

### P-07: Dependencia de macros VBA para validación

**Evidencia**: Botones "Ingreso total", "Ingreso subcódigo" y "Limpiar" controlados por VBA (63 KB de código binario).

**Problema**: Las reglas de negocio están embebidas en código opaco que no es auditable ni transferible. Si el archivo se corrompe, se pierden las validaciones.

### P-08: Dificultad para consultar históricos

**Evidencia**: Para obtener el código de paro más frecuente, se necesitaría recorrer 18 columnas por cada fila.

**Problema**: Las consultas cruzadas (ej. "paros por máquina y mes") requieren reestructurar los datos manualmente o usar tablas dinámicas complejas.

### P-09: Posibles duplicados

**Evidencia**: Se identificaron **42 filas potencialmente duplicadas** (igualdad exacta en 58 columnas).

**Problema**: Sin clave primaria formal, no hay mecanismo para prevenir duplicaciones.

---

## 2. Proceso de normalización

### 2.1 Estructura original (forma no normalizada — UNF)

La tabla `T_baseDeDatos` tiene esta estructura simplificada:

```
REGISTRO(
  Fecha, Mes, Año, Maquina, Operario, Referencia,
  UnidadesProducidasCadaMinuto, UnidadPorDisplay, DisplayPorPaca,
  PacasProducidas, HorasTrabajadas, Turno, HorasNoTrabajadas,
  TipoDeParo, ObservacionesDeParo,
  CodigoParo1, SubCodigo1, Codigo1EnHoras,
  CodigoParo2, Codigo2EnHoras,
  CodigoParo3, Subcod3, Codigo3EnHoras,
  CodigoParo4, Codigo4EnHoras,
  CodigoParo5, Subcod5, Codigo5EnHoras, AreaInvolucrada5, PersonalInvolucrado,
  CodigoParo6, Codigo6EnHoras,
  ... (hasta CodigoParo18, Codigo18EnHoras),
  TiempoDeParo, Observaciones
)
```

**Grupo repetitivo identificado**: `{CodigoParoN, CodigoNEnHoras}` para N = 1..18

**Dependencias funcionales parciales**: `Mes` y `Año` dependen de `Fecha`, no de la clave completa.

### 2.2 Primera Forma Normal (1FN)

**Requisito**: Eliminar grupos repetitivos. Cada celda debe contener un solo valor atómico.

**Problema**: Los 18 pares (CodigoParo_N, Codigo_N_EnHoras) son un grupo repetitivo.

**Transformación**: Se extrae el grupo repetitivo a una tabla independiente.

**Resultado**:

```
REGISTRO_PRODUCCION(
  id_registro PK,
  fecha, maquina, operario, referencia,
  pacas_producidas, horas_trabajadas, turno, horas_no_trabajadas,
  tipo_de_paro, observaciones_paro, tiempo_paro, observaciones
)

DETALLE_PARO(
  id_registro FK → REGISTRO_PRODUCCION,
  codigo_paro (1..18),
  duracion_minutos,
  PK(id_registro, codigo_paro)
)
```

**Anomalía eliminada**: Ya no hay columnas repetitivas. Agregar un código 19 solo requiere insertarlo en el catálogo; no cambia la estructura de tablas.

### 2.3 Segunda Forma Normal (2FN)

**Requisito**: Estar en 1FN y que todos los atributos no clave dependan de **toda** la clave primaria (eliminar dependencias parciales).

**Análisis de `DETALLE_PARO`**: La clave es (id_registro, codigo_paro). Los atributos `duracion_minutos` depende de toda la clave. ✅ Cumple 2FN.

**Análisis de `REGISTRO_PRODUCCION`**: La clave es id_registro (simple). No hay dependencias parciales posibles con clave simple. ✅ Cumple 2FN.

**Sin embargo**, se identifican entidades independientes que deben extraerse:

- `maquina` → debería referirse a un catálogo de máquinas
- `turno` → debería referirse a un catálogo de turnos
- `operario` → debería referirse a un catálogo de operarios
- `referencia` → debería referirse a un catálogo de productos
- `codigo_paro` → debería referirse a un catálogo de códigos

**Transformación**: Se crean tablas de catálogo.

```
MAQUINA(id_maquina PK, nombre, factor_produccion)
TURNO(id_turno PK, nombre, hora_inicio, hora_fin, duracion_horas)
OPERARIO(id_operario PK, nombre_pseudonimo)
REFERENCIA(id_referencia PK, nombre, presentacion)
CODIGO_PARO(id_codigo PK, numero, descripcion, area_impacto)
```

### 2.4 Tercera Forma Normal (3FN)

**Requisito**: Estar en 2FN y que no existan **dependencias transitivas** (un atributo no clave depende de otro atributo no clave).

**Dependencias transitivas detectadas**:

1. `Mes` y `Año` dependen de `Fecha` (transitiva a través de Fecha). **Solución**: No almacenar Mes y Año; se calculan con funciones SQL (MONTH(), YEAR()).

2. `Codigo_N_en_horas` depende de `Codigo_paro_N` (es Codigo_paro_N / 60). **Solución**: Almacenar solo minutos; calcular horas en consultas.

3. `UnidadesProducidasCadaMinuto`, `UnidadPorDisplay`, `DisplayPorPaca` dependen de la combinación (Máquina, Referencia), no del registro de producción. **Solución**: Mover a una tabla de metadatos de referencia-máquina.

**Transformación**:

```
REFERENCIA_MAQUINA(
  id_ref_maq PK,
  id_referencia FK,
  id_maquina FK,
  unidades_por_minuto,
  unidades_por_display,
  displays_por_paca,
  UNIQUE(id_referencia, id_maquina)
)
```

**Anomalías eliminadas**:
- **Actualización**: Cambiar las unidades por minuto de un producto se hace en un solo lugar, no en cada registro histórico
- **Inserción**: Se puede registrar un nuevo producto sin tener un registro de producción
- **Eliminación**: Borrar un registro de producción no pierde la información del producto

### 2.5 Subcódigos — Normalización adicional

**Estructura original**: En la tabla principal, los subcódigos están como columnas fijas (SubCodigo1, Subcod3, Subcod5). Además existe la tabla separada `Base_de_datos_subcodigos`.

**Transformación a 3FN**:

```
SUBCODIGO_PARO(
  id_subcodigo PK,
  id_codigo_padre FK → CODIGO_PARO,
  codigo_subcodigo,
  descripcion
)

DETALLE_SUBCODIGO(
  id_detalle_sub PK,
  id_registro FK → REGISTRO_PRODUCCION,
  id_subcodigo FK → SUBCODIGO_PARO,
  duracion_minutos,
  area_involucrada,
  personal_involucrado
)
```

**Justificación**: Un mismo registro puede tener múltiples subcódigos (como se evidencia en la tabla de subcódigos con múltiples filas por registro). La relación es 1:N entre registro y subcódigos.

### 2.6 Tipo de paro — Normalización

**Transformación**:

```
TIPO_PARO(
  id_tipo_paro PK,
  codigo,
  descripcion
)
```

El campo `tipo_de_paro` en REGISTRO_PRODUCCION pasa a ser una FK a esta tabla.

---

## 3. Resumen del esquema normalizado (3FN)

| Tabla | Forma Normal | Clave Primaria | Descripción |
|-------|-------------|----------------|-------------|
| maquina | 3FN | id_maquina | Catálogo de 4 líneas de envasado |
| turno | 3FN | id_turno | Catálogo de turnos de trabajo |
| operario | 3FN | id_operario | Personal de producción (pseudonimizado) |
| referencia | 3FN | id_referencia | Catálogo de productos |
| referencia_maquina | 3FN | id_ref_maq | Relación producto-máquina con métricas |
| codigo_paro | 3FN | id_codigo | Catálogo de 18 códigos de paro |
| subcodigo_paro | 3FN | id_subcodigo | Subcódigos (solo para 01, 03, 05) |
| tipo_paro | 3FN | id_tipo_paro | Catálogo de tipos de paro descriptivos |
| registro_produccion | 3FN | id_registro | Registro diario por máquina/turno |
| detalle_paro | 3FN | (id_registro, id_codigo) | Paros asociados a un registro |
| detalle_subcodigo | 3FN | id_detalle_sub | Subcódigos de un registro |

### Desnormalizaciones intencionales

Ninguna. El esquema se mantiene en 3FN completa. Los valores calculados (mes, año, horas de paro) se obtienen mediante funciones SQL.

