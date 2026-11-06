# 06 — Validación de la Migración

## Resumen cuantitativo

| Métrica | Valor |
|---------|-------|
| Total filas origen (CSV) | 8208 |
| Registros procesados | 8208 |
| Registros cargados exitosamente | 8208 |
| Registros rechazados | 0 |
| Detalles de paro generados | 16532 |
| Operarios únicos identificados | 32 |
| Referencias únicas | 51 |
| Tipos de paro únicos | 19 |

## Pseudonimización

- Se asignaron pseudónimos OP-001 a OP-032 a los operarios
- El mapeo real→pseudónimo se almacena en `migration/scripts/MAPEO_PRIVADO_NO_PUBLICAR.csv`
- Este archivo **NO debe subirse** al repositorio público
