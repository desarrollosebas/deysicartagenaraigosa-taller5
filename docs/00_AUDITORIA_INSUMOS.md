# 00 — Auditoría de Insumos (ACTUALIZADA)

> Documento generado como resultado de la FASE 0 del proyecto.  
> Auditoría inicial: 2026-11-03 | Actualización: 2026-11-03 (con paquete completo)

---

## 1. Inventario de archivos en el workspace

| # | Archivo | Presente | Relevancia |
|---|---------|----------|------------|
| 1 | `P-MTO-21-V1_Registro_paros_de_produccion_actividad.pdf` | ✅ | Procedimiento oficial P-MTO-22 V1 (7 págs.) |
| 2 | `SEGUIMIENTO TEMPERAS Y VINILOS Actividad(1).xlsm` | ✅ (en insumos) | **Insumo histórico principal** — Libro Excel con macros |
| 3 | `insumos_originales/` | ✅ | Extracción de insumos del Excel en CSV + reportes |

### Contenido del paquete de extracción

| Carpeta | Contenido |
|---------|-----------|
| `01_FUENTES_ORIGINALES/` | Copias del PDF y el XLSM |
| `02_EXTRACCION_EXCEL/CSV_POR_HOJA/` | 8 hojas exportadas a CSV |
| `02_EXTRACCION_EXCEL/REPORTES/` | Diagnóstico, inventario, fórmulas, frecuencias, duplicados |
| `02_EXTRACCION_EXCEL/` | `BASE_DATOS_T_BASEDATOS.csv` (tabla principal) y `BASE_DATOS_SUBCODIGOS.csv` |
| `03_PDF_PAGINAS/` | Imágenes de cada página del PDF |
| `04_REFERENCIAS/` | Manifiesto de archivos |

---

## 2. Hallazgos del análisis del Excel

### 2.1 Estructura general

- **21 hojas** en total, **4 ocultas** (Calculadora de tiempos, Base de datos de Sub codigos, TABLA CODIGOS, Hoja4)
- **23 tablas estructuradas** de Excel
- **180,159 celdas con fórmula**
- Proyecto VBA presente (63,488 bytes) — no ejecutado ni descompilado

### 2.2 Tabla principal: `T_baseDeDatos`

- **Rango**: A9:BF8217 → **58 columnas**, **8,208 filas de datos**
- **Período**: 2022-01-01 a 2025-03-28 (más de 3 años de historia)
- **Columnas**: Fecha, Mes, Año, Máquina, Operario, Referencia, Unidades producidas cada minuto, Unidad por display, Display por paca, Pacas producidas, Horas trabajadas, Turno, Horas no trabajadas, Tipo de paro, Observaciones de paro, + 18 pares de (Código de paro N / Código N en horas), Sub Código 1, Subcodigo 3, Subcodigo 5, Área involucrada en subcódigo 5, Personal involucrado, Tiempo de Paro, Observaciones

### 2.3 Tabla de subcódigos: `Base_de_datos_subcodigos`

- **Rango**: A8:S1260 → **19 columnas**, **1,252 filas**
- **Período**: 2023-10-25 a 2024-05-29
- Campos: Fecha, Mes, Año, Máquina, Operario, Referencia, Pacas producidas, Turno, + pares (Código/Subcódigo/Horas) para códigos 1, 3 y 5, Área involucrada, Personal involucrado

### 2.4 Distribución por máquina

| Máquina | Registros |
|---------|-----------|
| Vinilos_4 | 2,585 |
| Vinilos_3 | 2,491 |
| Vinilos_1 | 1,877 |
| Vinilos_2 | 1,255 |

### 2.5 Distribución por turno

| Turno | Registros |
|-------|-----------|
| 6am-2pm (Turno 1) | 1,352 |
| 2pm-10pm (Turno 2) | 1,182 |
| 10pm-6am (Turno 3) | 1,012 |
| 6am-4:30pm | 359 |
| No aplica | 336 |
| 6am-6pm | 35 |
| 6pm-6am | 20 |

### 2.6 Tipos de paro (campo descriptivo)

| Tipo de paro | Registros |
|-------------|-----------|
| [19] No aplica | 2,282 |
| 17. PARO DE MAQUINA | 952 |
| [18] Paro de maquina por ventas | 605 |
| 9.FALTA DE PROGRAMACIÓN (PLANEACIÓN) | 251 |
| 16. PARO POR PROCESO ANTERIOR | 94 |
| 10. PARO POR MATERIA PRIMA O MATERIAL NO CONFORME | 66 |
| 6. FALTA DE MATERIALES O MATERIAS PRIMAS | 61 |
| [14] Falta de materia prima | 50 |
| 15. APROBACION DE LABORATORIO | 24 |
| [09] Falta de operario | 8 |
| [05] Ajuste operativo | 7 |
| Otros | ~26 |

> **Hallazgo importante**: Coexisten DOS sistemas de nomenclatura para los tipos de paro: uno antiguo (números sin corchetes, e.g., "17. PARO DE MAQUINA") y uno nuevo (con corchetes, e.g., "[18] Paro de maquina por ventas"). Esto indica una evolución del catálogo durante los 3+ años de historia.

### 2.7 Datos de calidad

| Indicador | Valor |
|-----------|-------|
| Filas con Pacas producidas | 5,157 |
| Filas sin Pacas producidas | 3,051 |
| Filas con Operario informado | 4,487 |
| Filas sin Operario | 3,721 |
| Filas con Turno informado | 4,296 |
| Filas sin Turno | 3,912 |
| Valores distintos de Operario | 34 (incluye "No" y "No aplica") |
| Posibles duplicados exactos | 42 |
| Errores #VALUE! en celdas | 588 |
| Errores #N/A | 27 |

### 2.8 Fórmula de eficiencia/productividad

De la hoja "Tiempos":
```
Eficiencia = IF(producción_real = 0, 0, (producción_real / producción_ideal) * fProduccion)
```
Donde:
- `producción_ideal = horas_trabajadas × meta_por_hora`
- `producción_real = pacas_producidas`
- `fProduccion` = Factor de producción por máquina (Tiempos!C7)

El factor de producción varía según la máquina:
- Vinilos_1: 1.1
- Vinilos_2: 1.16
- Vinilos_3: 1
- Vinilos_4: 1

### 2.9 Catálogos identificados

**18 códigos de paro** con área de impacto:
- Códigos 01-04: Mantenimiento
- Códigos 05-11: Producción  
- Códigos 12-13: Calidad
- Código 14: Almacén de materias primas
- Códigos 15-17: Paro programado

**Subcódigos** (solo para códigos 01, 03 y 05):
- Código 01: ~20 subcódigos (sistema alimentador, dosificación, banda, tapado, video jet, sujeción, etiquetadora)
- Código 03: 5 subcódigos (subestación, red pública, neumática, enfriamiento, vapor)
- Código 05: 11 subcódigos (alimentador envases, dosificación, bandas, transfer, video jet, etiquetado, purga, lavado)

**Operarios**: ~44 nombres (listados en hoja Tiempos columna S)

**Referencias por máquina**: ~50 referencias por máquina (productos como Parchesitos, Pintorcitos, Klips, etc.)

### 2.10 Nombres definidos clave

| Nombre | Referencia | Uso |
|--------|-----------|-----|
| fProduccion | Tiempos!$C$7 | Factor de producción (varía por máquina) |
| maquina | Registro!$C$3 | Máquina seleccionada |
| operario | Registro!$C$6 | Operario seleccionado |
| turno | Registro!$C$4 | Turno seleccionado |
| codes | Registro!$I$3:$I$20 + $E$16 | Todos los campos de código |
| tiempoFaltante | Tiempos!$C$15 | Tiempo sin reportar |
| Subcodigos1/3/5 | Tablas de subcódigos | Listas desplegables |

---

## 3. Discrepancias y contradicciones

| # | Discrepancia | Decisión |
|---|-------------|----------|
| D-01 | Archivo P-MTO-21 vs. documento P-MTO-22 | Se usa P-MTO-22 V1 como referencia |
| D-02 | Texto lista 17 códigos vs. formulario muestra 18 | Se usan **18 códigos** (01-18) |
| D-03 | Código 18 en PDF = "Desinfección" vs. Excel = "Paro de máquina por ventas" | **Discrepancia real** — se preservan ambos significados |
| D-04 | "[19] No aplica" como tipo de paro | Es un valor especial = "sin paro programado" |
| D-05 | Dos sistemas de nomenclatura de tipos de paro | Sistema antiguo (sin corchetes) y nuevo (con corchetes) coexisten |
| D-06 | Factor de producción difiere por máquina | Vinilos_1: 1.1, Vinilos_2: 1.16, Vinilos_3 y 4: 1.0 |
| D-07 | 7 variantes de turno (3 estándar + 4 especiales) | Necesita normalización en el catálogo |

---

## 4. Datos personales identificados

- **Columna `Operario`**: ~34 nombres (primeros nombres y/o iniciales de apellido)
- **Campo `Personal involucrado`**: nombres completos de personal de mantenimiento
- **Hoja Tiempos, columna S**: lista completa de operarios (~44 nombres)
- **Formato manual en PDF**: nombres manuscritos visibles

> **Acción requerida**: Pseudonimización antes de publicar en repositorio público.

---

## 5. Decisiones confirmadas

| Decisión | Valor |
|----------|-------|
| Motor de BD | **MySQL** |
| Integrante 1 | Juan Sebastián Raigosa Gil (desarrollosebas) |
| Integrante 2 | Deysi Carolina Echavarría Soto (CarolinaSoto22) |
| Integrante 3 | Jose Miguel Sosa Cartagena (josesosa216-pb) |
| Guía del profesor | Lo indicado en la guía de la actividad entregada en clase |
| Excel disponible | ✅ Sí (en paquete de extracción) |
