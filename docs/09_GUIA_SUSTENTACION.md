# 09 — Guía de Sustentación

> Guía para que los tres integrantes (Juan Sebastián Raigosa Gil, Deysi Carolina Echavarría Soto y Jose Miguel Sosa Cartagena) puedan explicar y defender cualquier parte del proyecto.

---

## 1. Recorrido completo del proyecto (5 minutos)

### Flujo narrativo recomendado:

1. **"El problema"**: La empresa tiene 4 máquinas de envasado. Las operarias llenan un formato en papel, que se transcribe a un Excel con macros. El Excel tiene 8,200+ registros en 58 columnas.

2. **"Los problemas del Excel"**: 
   - 18 códigos de paro como columnas repetidas (36 columnas)
   - Sin integridad referencial (cualquier texto en cualquier campo)
   - Datos calculados almacenados redundantemente
   - Reglas de negocio ocultas en macros VBA

3. **"La solución"**: Base de datos relacional en MySQL con 11 tablas normalizadas hasta 3FN.

4. **"El resultado"**: 8,208 registros migrados, 16,532 detalles de paro, 10 consultas de negocio, protección de datos personales.

---

## 2. Explicación de cada entidad

### ¿Por qué existe la tabla `maquina`?
> Porque las 4 líneas de envasado son un dato maestro que se repite en miles de registros. En vez de escribir "Vinilos_1" 1,877 veces (como en el Excel), se almacena una vez y se referencia con un ID. Además, cada máquina tiene un factor de producción propio.

### ¿Por qué existe la tabla `turno`?
> Porque los turnos tienen atributos propios (hora inicio, hora fin, minutos de alimentación). En el Excel eran texto libre con 7 variantes inconsistentes.

### ¿Por qué existe la tabla `detalle_paro`?
> Porque los 18 códigos de paro estaban como **grupo repetitivo** (36 columnas). Al normalizarlos a filas, cada paro es un registro independiente con solo 3 campos: id_registro, id_codigo, duracion_minutos. Esto elimina la violación de 1FN.

### ¿Por qué `operario` solo tiene pseudónimo?
> Para proteger la información personal. Los nombres reales se almacenan en un archivo separado que no se publica en GitHub.

---

## 3. Normalización paso a paso

### Si el profesor pregunta: "¿Cómo demostraste que está en 1FN?"

> "Identificamos que la tabla original tiene un **grupo repetitivo**: 18 pares de columnas (CodigoParo_N, Codigo_N_EnHoras). Para cumplir 1FN, extrajimos ese grupo a la tabla `detalle_paro`, donde cada código es una **fila** independiente con clave compuesta (id_registro, id_codigo)."

### Si pregunta: "¿Cómo demostraste 2FN?"

> "En la tabla `detalle_paro`, la clave compuesta es (id_registro, id_codigo). El único atributo no clave es `duracion_minutos`, que depende de **ambas partes** de la clave (necesitas saber cuál registro y cuál código para conocer la duración). No hay dependencias parciales."

### Si pregunta: "¿Cómo demostraste 3FN?"

> "Eliminamos las dependencias transitivas: 
> - `Mes` y `Año` dependían de `Fecha` → se calculan con MONTH() y YEAR() en SQL
> - `Codigo_N_en_horas` dependía de `Codigo_N_en_minutos` (÷60) → se almacenan solo minutos
> - Los atributos de producto (unidades_por_minuto) dependían de la combinación (máquina, referencia), no del registro → se movieron a la tabla `referencia_maquina`"

---

## 4. Justificación de restricciones

### Si pregunta: "¿Por qué usaste ON DELETE CASCADE en detalle_paro?"

> "Porque un detalle de paro **no tiene sentido** sin su registro padre. Si se elimina un registro de producción, sus detalles de paro deben eliminarse automáticamente para no dejar datos huérfanos."

### Si pregunta: "¿Por qué ON DELETE RESTRICT en la FK de maquina?"

> "Porque no queremos que alguien borre una máquina si hay registros históricos asociados. Los datos de producción son evidencia histórica que no debe perderse accidentalmente."

### Si pregunta: "¿Por qué ON DELETE SET NULL en operario?"

> "Porque un operario puede retirarse de la empresa, pero sus registros de producción históricos deben conservarse. Al poner SET NULL, el registro se mantiene sin enlace al operario, pero no se pierde la fecha, máquina, producción ni paros."

### Si pregunta: "¿Por qué el CHECK en factor_produccion > 0?"

> "Porque el factor de producción se usa como multiplicador en la fórmula de eficiencia. Un factor negativo o cero produciría resultados sin sentido. La restricción CHECK lo previene a nivel de base de datos."

---

## 5. Consultas — Cómo explicarlas

### Consulta 1 (Productividad):
> "Calcula el porcentaje de tiempo productivo por máquina y mes. Hace un JOIN con la tabla de máquinas para obtener el nombre, una subconsulta para sumar los minutos de paro por registro, y agrupa por máquina/año/mes. El filtro BETWEEN limita el rango de fechas."

### Consulta 3 (Subcódigos):
> "Usa tres INNER JOINs: detalle_subcodigo → subcodigo_paro → codigo_paro. Filtra por los códigos 01, 03 y 05. Agrupa por subcódigo y usa HAVING para excluir subcódigos sin duración. La subconsulta calcula el porcentaje dentro de cada código padre."

### Consulta 4 (Turnos):
> "Usa un LEFT JOIN con una subconsulta de totales de paro para incluir registros sin paros. Agrupa por turno y calcula el promedio de productividad. Excluye el turno 'No aplica'."

---

## 6. Procedimiento para demostración en vivo

1. Abrir DBeaver
2. Verificar conexión a MySQL (`SELECT VERSION()`)
3. Ejecutar `00_crear_base_datos.sql`
4. Ejecutar `01_crear_tablas.sql` → mostrar las tablas creadas
5. Ejecutar `02_datos_catalogos.sql` → mostrar `SELECT * FROM codigo_paro`
6. Ejecutar los scripts de carga (04-07)
7. Ejecutar `09_pruebas_restricciones.sql` → mostrar conteos y verificaciones
8. **Demostración de rechazo**: descomentar una prueba negativa y mostrar el error
9. Ejecutar consulta 1 → explicar el resultado
10. Ejecutar consulta 2 → comparar con el gráfico del PDF

---

## 7. Preguntas difíciles y respuestas

### "¿Por qué no usaron PostgreSQL?"

> "MySQL fue la elección porque es el motor que manejamos y tiene soporte completo para CHECK constraints desde la versión 8.0.16. Para un proyecto académico con 8,000 registros, ambos motores son equivalentes en funcionalidad."

### "¿Qué pasa si la empresa agrega una quinta máquina?"

> "Solo se inserta una fila en la tabla `maquina`. No se modifica ninguna tabla ni consulta. En el Excel habría que agregar columnas y modificar todas las fórmulas y macros."

### "¿Qué pasa si agregan un código de paro 19?"

> "Se inserta una fila en `codigo_paro`. Ampliamos el CHECK de 1-18 a 1-19. No se agregan columnas ni se modifican las consultas."

### "¿Por qué hay filas sin Pacas producidas?"

> "En el Excel original, 3,051 de 8,208 filas no tienen este campo. Puede deberse a: (a) registros de subcódigo que son extensiones del registro principal, (b) turnos donde no hubo producción, o (c) datos incompletos de la transcripción manual."

### "¿Cómo protegieron los datos personales?"

> "Pseudonimización: cada nombre real se reemplazó por un código (OP-001, OP-002, etc.). El mapeo se almacena en un archivo local que NO se sube a GitHub. El .gitignore excluye el archivo xlsm original, el mapeo y cualquier archivo con datos personales."

### "¿Qué anomalías de la base de datos detectaron?"

> "Tres tipos: 
> - **Inserción**: en el Excel, no podías registrar un nuevo producto sin crear un registro de producción completo. En la BD, puedes insertar en la tabla `referencia` independientemente.
> - **Actualización**: si cambiaba la descripción de un código, había que buscar en 8,000 filas. Ahora se actualiza en un solo lugar (`codigo_paro`).
> - **Eliminación**: si borrabas una fila del Excel, perdías el dato del producto. Con ON DELETE SET NULL, el producto se puede descontinuar sin perder los registros históricos."

---

## 8. Ejercicios para practicar

### Modificar la Consulta 1 para ver solo Vinilos_3:
```sql
-- Agregar al WHERE:
AND m.nombre = 'Vinilos_3'
```

### Modificar la Consulta 2 para ver solo códigos de Mantenimiento:
```sql
-- Agregar al WHERE:
AND cp.area_impacto = 'Mantenimiento'
```

### Agregar un nuevo registro en vivo:
```sql
INSERT INTO registro_produccion 
    (fecha, id_maquina, id_turno, id_operario, horas_trabajadas, pacas_producidas)
VALUES ('2025-04-15', 2, 1, 5, 8.0, 200);
```

### Intentar una violación para demostrar restricciones:
```sql
-- Esto debe fallar:
INSERT INTO maquina (nombre, factor_produccion) VALUES ('Vinilos_1', 1.0);
-- Error: Duplicate entry 'Vinilos_1' for key 'uq_maquina_nombre'
```

