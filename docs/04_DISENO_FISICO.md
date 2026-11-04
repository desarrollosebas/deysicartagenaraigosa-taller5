# 04 — Diseño Físico

> Motor: **MySQL 8.x** | Esquema: `paros_produccion` | Herramienta: DBeaver

---

## 1. Justificación del motor MySQL

Se eligió **MySQL** por:
- **Familiaridad**: es el motor que manejan los integrantes del equipo
- **Compatibilidad con DBeaver**: integración nativa completa
- **Soporte CHECK**: MySQL 8.0.16+ soporta restricciones CHECK funcionales
- **Rendimiento adecuado**: para ~8,000 registros históricos es más que suficiente
- **Disponibilidad**: instalación sencilla en Windows

## 2. Modelo Entidad-Relación (notación pata de gallo)

```mermaid
erDiagram
    maquina ||--o{ registro_produccion : "produce en"
    turno ||--o{ registro_produccion : "trabaja en"
    operario ||--o{ registro_produccion : "opera"
    referencia ||--o{ registro_produccion : "fabrica"
    tipo_paro ||--o{ registro_produccion : "clasifica"
    
    maquina ||--o{ referencia_maquina : "tiene"
    referencia ||--o{ referencia_maquina : "se fabrica en"
    
    registro_produccion ||--o{ detalle_paro : "tiene paros"
    codigo_paro ||--o{ detalle_paro : "clasifica"
    
    codigo_paro ||--o{ subcodigo_paro : "se desglosa en"
    registro_produccion ||--o{ detalle_subcodigo : "tiene subcódigos"
    subcodigo_paro ||--o{ detalle_subcodigo : "detalla"

    maquina {
        SMALLINT id_maquina PK
        VARCHAR nombre UK
        DECIMAL factor_produccion
        BOOLEAN activa
    }
    
    turno {
        SMALLINT id_turno PK
        VARCHAR nombre UK
        TIME hora_inicio
        TIME hora_fin
        DECIMAL duracion_horas
        SMALLINT minutos_alimentacion
        SMALLINT minutos_pausa
    }
    
    operario {
        SMALLINT id_operario PK
        VARCHAR pseudonimo UK
        BOOLEAN activo
    }
    
    referencia {
        SMALLINT id_referencia PK
        VARCHAR nombre UK
    }
    
    referencia_maquina {
        INT id_ref_maq PK
        SMALLINT id_referencia FK
        SMALLINT id_maquina FK
        DECIMAL unidades_por_minuto
        SMALLINT unidades_por_display
        SMALLINT displays_por_paca
    }
    
    codigo_paro {
        SMALLINT id_codigo PK
        TINYINT numero UK
        VARCHAR descripcion
        VARCHAR area_impacto
        BOOLEAN tiene_subcodigos
    }
    
    subcodigo_paro {
        SMALLINT id_subcodigo PK
        SMALLINT id_codigo_padre FK
        VARCHAR codigo
        VARCHAR descripcion
    }
    
    tipo_paro {
        SMALLINT id_tipo_paro PK
        VARCHAR codigo
        VARCHAR descripcion UK
    }
    
    registro_produccion {
        INT id_registro PK
        DATE fecha
        SMALLINT id_maquina FK
        SMALLINT id_turno FK
        SMALLINT id_operario FK
        SMALLINT id_referencia FK
        DECIMAL horas_trabajadas
        DECIMAL meta_por_hora
        INT pacas_producidas
        DECIMAL horas_no_trabajadas
        SMALLINT id_tipo_paro FK
        TEXT observaciones_paro
        DECIMAL tiempo_paro_minutos
        TEXT observaciones
    }
    
    detalle_paro {
        INT id_registro PK_FK
        SMALLINT id_codigo PK_FK
        DECIMAL duracion_minutos
    }
    
    detalle_subcodigo {
        INT id_detalle_sub PK
        INT id_registro FK
        SMALLINT id_subcodigo FK
        DECIMAL duracion_minutos
        VARCHAR area_involucrada
        VARCHAR personal_involucrado
    }
```

## 3. Justificación de índices

| Índice | Tabla | Columnas | Justificación |
|--------|-------|----------|---------------|
| idx_reg_fecha | registro_produccion | fecha | Todas las consultas filtran por rango de fechas |
| idx_reg_maquina_fecha | registro_produccion | id_maquina, fecha | Consulta 1: productividad por máquina y mes |
| idx_reg_turno | registro_produccion | id_turno | Consulta 4: comparación entre turnos |
| idx_dp_codigo | detalle_paro | id_codigo | Consultas 2, 7: agregación por código |
| idx_ds_subcodigo | detalle_subcodigo | id_subcodigo | Consulta 3: análisis de subcódigos |
| idx_reg_operario | registro_produccion | id_operario | Consulta 10: rendimiento por operario |

## 4. Políticas ON DELETE / ON UPDATE

| FK | ON DELETE | ON UPDATE | Justificación |
|----|----------|-----------|---------------|
| reg → maquina | RESTRICT | CASCADE | No se permite borrar una máquina con datos. Si se renombra, se propaga. |
| reg → turno | RESTRICT | CASCADE | No se permite borrar un turno con datos. |
| reg → operario | SET NULL | CASCADE | Un operario puede retirarse; sus registros se conservan sin enlace. |
| reg → referencia | SET NULL | CASCADE | Un producto puede descontinuarse; los registros se conservan. |
| reg → tipo_paro | SET NULL | CASCADE | Flexibilidad para modificar el catálogo de tipos. |
| detalle_paro → reg | CASCADE | CASCADE | Al borrar un registro, sus detalles se eliminan automáticamente. |
| detalle_paro → codigo | RESTRICT | CASCADE | No se permite borrar un código con datos. |
| detalle_sub → reg | CASCADE | CASCADE | Cascada coherente con detalle_paro. |
| detalle_sub → subcodigo | RESTRICT | CASCADE | Proteger el catálogo de subcódigos. |

