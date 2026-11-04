# Modelo Conceptual — Entidad-Relación

## Diagrama ER (notación pata de gallo)

```mermaid
erDiagram
    MAQUINA ||--o{ REGISTRO_PRODUCCION : "produce en"
    TURNO ||--o{ REGISTRO_PRODUCCION : "trabaja en"
    OPERARIO ||--o{ REGISTRO_PRODUCCION : "opera"
    REFERENCIA ||--o{ REGISTRO_PRODUCCION : "fabrica"
    TIPO_PARO ||--o{ REGISTRO_PRODUCCION : "clasifica"
    
    MAQUINA ||--o{ REFERENCIA_MAQUINA : "fabrica"
    REFERENCIA ||--o{ REFERENCIA_MAQUINA : "se produce en"
    
    REGISTRO_PRODUCCION ||--o{ DETALLE_PARO : "tiene paros"
    CODIGO_PARO ||--o{ DETALLE_PARO : "identifica"
    
    CODIGO_PARO ||--o{ SUBCODIGO_PARO : "se detalla en"
    REGISTRO_PRODUCCION ||--o{ DETALLE_SUBCODIGO : "se analiza en"
    SUBCODIGO_PARO ||--o{ DETALLE_SUBCODIGO : "especifica"

    MAQUINA {
        int id_maquina PK
        string nombre
        decimal factor_produccion
        boolean activa
    }
    
    TURNO {
        int id_turno PK
        string nombre
        time hora_inicio
        time hora_fin
        decimal duracion_horas
        int minutos_alimentacion
        int minutos_pausa
    }
    
    OPERARIO {
        int id_operario PK
        string pseudonimo
        boolean activo
    }
    
    REFERENCIA {
        int id_referencia PK
        string nombre
    }
    
    REFERENCIA_MAQUINA {
        int id_ref_maq PK
        int id_referencia FK
        int id_maquina FK
        decimal unidades_por_minuto
        int unidades_por_display
        int displays_por_paca
    }
    
    CODIGO_PARO {
        int id_codigo PK
        int numero
        string descripcion
        string area_impacto
        boolean tiene_subcodigos
    }
    
    SUBCODIGO_PARO {
        int id_subcodigo PK
        int id_codigo_padre FK
        string codigo
        string descripcion
    }
    
    TIPO_PARO {
        int id_tipo_paro PK
        string codigo
        string descripcion
    }
    
    REGISTRO_PRODUCCION {
        int id_registro PK
        date fecha
        int id_maquina FK
        int id_turno FK
        int id_operario FK
        int id_referencia FK
        decimal horas_trabajadas
        decimal meta_por_hora
        int pacas_producidas
        decimal horas_no_trabajadas
        int id_tipo_paro FK
        text observaciones_paro
        decimal tiempo_paro_minutos
        text observaciones
    }
    
    DETALLE_PARO {
        int id_registro PK_FK
        int id_codigo PK_FK
        decimal duracion_minutos
    }
    
    DETALLE_SUBCODIGO {
        int id_detalle_sub PK
        int id_registro FK
        int id_subcodigo FK
        decimal duracion_minutos
        string area_involucrada
        string personal_involucrado
    }
```

## Entidades y sus relaciones

| Entidad | Tipo | Cardinalidad | Descripción |
|---------|------|-------------|-------------|
| MAQUINA → REGISTRO_PRODUCCION | 1:N | Obligatoria | Cada registro pertenece a una máquina |
| TURNO → REGISTRO_PRODUCCION | 1:N | Obligatoria | Cada registro pertenece a un turno |
| OPERARIO → REGISTRO_PRODUCCION | 1:N | Opcional | Un registro puede no tener operario asignado |
| REFERENCIA → REGISTRO_PRODUCCION | 1:N | Opcional | Un registro puede no tener referencia |
| TIPO_PARO → REGISTRO_PRODUCCION | 1:N | Opcional | Tipo de paro a nivel de turno |
| MAQUINA ↔ REFERENCIA | N:M | (vía REFERENCIA_MAQUINA) | Qué productos se fabrican en cada máquina |
| REGISTRO_PRODUCCION → DETALLE_PARO | 1:N | Opcional | Desglose de paros por código |
| CODIGO_PARO → DETALLE_PARO | 1:N | Obligatoria | Cada detalle referencia un código |
| CODIGO_PARO → SUBCODIGO_PARO | 1:N | Solo cod 01,03,05 | Subcódigos de detalle |
| REGISTRO_PRODUCCION → DETALLE_SUBCODIGO | 1:N | Opcional | Detalle de subcódigos |
| SUBCODIGO_PARO → DETALLE_SUBCODIGO | 1:N | Obligatoria | Cada detalle referencia un subcódigo |

