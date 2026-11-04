"""
04_migrar_datos.py
Script de migración de datos del Excel (CSV extraído) a sentencias SQL INSERT.
Lee los CSV sin modificar los archivos originales.
Genera archivos SQL con los datos migrados y pseudonimizados.

Uso: python migration/scripts/04_migrar_datos.py
"""

import csv
import os
import re
from collections import OrderedDict

# Rutas
BASE = r"c:\Users\Sebas\Desktop\Bases datos 1\TRABAJO2"
CSV_DIR = os.path.join(BASE, "Paquete_Claude_Control_Produccion",
                       "Paquete_Claude_Control_Produccion", "02_EXTRACCION_EXCEL")
OUTPUT_DIR = os.path.join(BASE, "sql")

# Archivo principal
MAIN_CSV = os.path.join(CSV_DIR, "BASE_DATOS_T_BASEDATOS.csv")
SUB_CSV = os.path.join(CSV_DIR, "BASE_DATOS_SUBCODIGOS.csv")

# ---- Pseudonimización ----
operarios_map = OrderedDict()
personal_map = OrderedDict()
op_counter = [0]
pers_counter = [0]

def pseudonimizar_operario(nombre):
    """Reemplaza nombres reales por pseudónimos OP-NNN."""
    if not nombre or nombre.strip() == '' or nombre.strip().lower() in ('no aplica', 'no', ''):
        return None
    nombre = nombre.strip()
    if nombre not in operarios_map:
        op_counter[0] += 1
        operarios_map[nombre] = f"OP-{op_counter[0]:03d}"
    return operarios_map[nombre]

def pseudonimizar_personal(nombre):
    """Reemplaza nombres de personal de mantenimiento por PM-NNN."""
    if not nombre or nombre.strip() == '' or nombre.strip().lower() in ('no aplica', 'no', ''):
        return None
    nombre = nombre.strip()
    if nombre not in personal_map:
        pers_counter[0] += 1
        personal_map[nombre] = f"PM-{pers_counter[0]:03d}"
    return personal_map[nombre]

# ---- Catálogos ----
maquinas_map = {
    'Vinilos_1': 1, 'Vinilos_2': 2, 'Vinilos_3': 3, 'Vinilos_4': 4
}

turnos_map = {
    '6am-2pm (Turno 1)': 1, '2pm-10pm (Turno 2)': 2, '10pm-6am (Turno 3)': 3,
    '6am-4:30pm': 4, '6am-6pm': 5, '6pm-6am': 6, 'No aplica': 7
}

referencias = OrderedDict()
ref_counter = [0]

def get_referencia_id(nombre):
    if not nombre or nombre.strip() == '' or nombre.strip().lower() == 'no aplica':
        return None
    nombre = nombre.strip()
    if nombre not in referencias:
        ref_counter[0] += 1
        referencias[nombre] = ref_counter[0]
    return referencias[nombre]

# Tipos de paro
tipos_paro = OrderedDict()
tp_counter = [0]

def get_tipo_paro_id(valor):
    if not valor or valor.strip() == '':
        return None
    valor = valor.strip()
    if valor not in tipos_paro:
        tp_counter[0] += 1
        tipos_paro[valor] = tp_counter[0]
    return tipos_paro[valor]

# Subcódigos conocidos del catálogo (id_subcodigo asignados por el INSERT del 02_datos_catalogos.sql)
# Se mapean por texto descriptivo del subcódigo
subcodigos_map = {}

def build_subcodigo_map():
    """Construye el mapeo de textos de subcódigo a IDs."""
    # Código 01: IDs 1-31
    sub01 = {
        '1.1 SISTEMA ALIMENTADOR DE ENVASES': 1, '1.1 Sistema alimentador de envases': 1,
        '1.1.A Banda': 2, '1.1.B Motor': 3, '1.1.B  Motor': 3,
        '1.1.C Sensor': 4, '1.1.C  Sensor': 4,
        '1.2 SISTEMA DE DOSIFICACIÓN': 5, '1.2 Sistema de dosificación': 5,
        '1.2.A Cambio de racores': 6, '1.2.B Ajuste de sensor': 7,
        '1.2.C Cambio de Valvula': 8, '1.2.C Cambio de valvula': 8, '1.2.C Cambio de válvula': 8,
        '1.2.D Retenedores': 9, '1.2.E O\'Ring': 10, '1.2.E O\'ring': 10,
        '1.3 Sistema de banda de entrada': 11, '1.3.A Banda': 12, '1.3.B Motor': 13,
        '1.4 Sistema de tapado': 14, '1.4.A Motor del transfer': 15,
        '1.4.B Pisador de tapa': 16, '1.4.3 Sensor': 17,
        '1.5 Sistema de alimentación de tapa': 18, '1.5 SISTEMA DE ALIMENTACIÓN DE TAPA': 18,
        '1.5.A Banda': 19, '1.5.B Motor': 20, '1.5.C Sensor': 21,
        '1.6 Sistema Video Jet': 22, '1.6 SISTEMA VIDEO JET': 22,
        '1.6.A Fotocelda': 23, '1.6.B Sensor': 24, '1.6.E Sensor': 24,
        '1.7 Sistema de sujeción y roscadores': 25,
        '1.7.A Banda de sujeción': 26, '1.7.B Roscadores': 27,
        '1.8 Sistema etiquetadora': 28, '1.8.A Banda': 29, '1.8.B Motor': 30, '1.8.C Sensor': 31,
    }
    # Código 03: IDs 32-36
    sub03 = {
        '3.1 Fallo en la subestación': 32, '3.1 Falla en la red neumática o el compresor': 35,
        '3.2 Fallo en la red pública': 33, '3.2 Fallo en la red publica': 33,
        '3.3 Falla en la red neumática o el compresor': 35,
        '3.4 Falla en la red de enfriamiento o el chiller': 36,
        '3.5 Falla en la red de vapor o la caldera': 36,
    }
    # Código 05: IDs 37-47
    sub05 = {
        '5.1 Sistema alimentador de envases': 37,
        '5.2 Sistema de dosificación de pintura, frontal posterior': 38,
        '5.3 Banda transportadora de entrada': 39,
        '5.4 Banda transportadora de salida': 40,
        '5.5 Transfer y pisador de tapa': 41,
        '5.6 Sistema alimentador de tapa y tobogan': 42, '5.6 Sistema alimentador de tapa y tobogán': 42,
        '5.7 Video Jet': 43, '5.8 Banda de sujeción y roscadores': 44,
        '5.9 Sistema de etiquetado': 45, '5.10 Purga de color': 46,
        '5.11 Lavado de boquilla': 47,
    }
    subcodigos_map.update(sub01)
    subcodigos_map.update(sub03)
    subcodigos_map.update(sub05)

def find_subcodigo_id(texto):
    """Busca el ID de un subcódigo por texto."""
    if not texto or texto.strip() == '' or texto.strip() == ' ':
        return None
    texto = texto.strip()
    if texto in subcodigos_map:
        return subcodigos_map[texto]
    # Búsqueda parcial
    for key, val in subcodigos_map.items():
        if texto.lower() in key.lower() or key.lower() in texto.lower():
            return val
    return None

def safe_decimal(val):
    """Convierte un valor a decimal o retorna None."""
    if val is None or str(val).strip() == '' or str(val).strip() == ' ':
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

def safe_int(val):
    """Convierte un valor a entero o retorna None."""
    if val is None or str(val).strip() == '' or str(val).strip() == ' ':
        return None
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return None

def sql_str(val):
    """Escapa un valor string para SQL."""
    if val is None:
        return 'NULL'
    val = str(val).replace("'", "''").replace("\\", "\\\\")
    return f"'{val}'"

def sql_num(val):
    """Formatea un número para SQL."""
    if val is None:
        return 'NULL'
    return str(val)

# ---- Main ----
def main():
    build_subcodigo_map()
    
    # Contadores
    total_rows = 0
    loaded_rows = 0
    rejected_rows = 0
    rejected_reasons = []
    
    registros_sql = []
    detalles_paro_sql = []
    
    print("Leyendo datos principales...")
    with open(MAIN_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            
            # Validar fecha
            fecha = row.get('Fecha', '').strip()
            if not fecha or fecha == '' or fecha == ' ':
                rejected_rows += 1
                rejected_reasons.append(f"Fila {total_rows}: Sin fecha")
                continue
            
            # Mapear máquina
            maquina = row.get('Maquina', '').strip()
            id_maquina = maquinas_map.get(maquina)
            if id_maquina is None:
                rejected_rows += 1
                rejected_reasons.append(f"Fila {total_rows}: Máquina desconocida '{maquina}'")
                continue
            
            # Mapear turno
            turno = row.get('Turno', '').strip()
            id_turno = turnos_map.get(turno)
            if not turno or turno == '' or turno == ' ':
                id_turno = turnos_map['No aplica']
            elif id_turno is None:
                rejected_rows += 1
                rejected_reasons.append(f"Fila {total_rows}: Turno desconocido '{turno}'")
                continue
            
            # Pseudonimizar operario
            op_name = row.get('Operario', '').strip()
            pseudo = pseudonimizar_operario(op_name)
            
            # Referencia
            ref_name = row.get('Referencia', '').strip()
            id_ref = get_referencia_id(ref_name)
            
            # Tipo de paro
            tipo = row.get('Tipo de paro', '').strip()
            id_tp = get_tipo_paro_id(tipo) if tipo and tipo != '' else None
            
            # Valores numéricos
            horas_trab = safe_decimal(row.get('Horas trabajadas'))
            meta = safe_decimal(row.get('', None))  # meta_por_hora no está directamente en CSV
            pacas = safe_int(row.get('Pacas producidas'))
            horas_no_trab = safe_decimal(row.get('Horas no trabajadas'))
            obs_paro = row.get('Observaciones de paro', '').strip()
            tiempo_paro = safe_decimal(row.get('Tiempo de Paro'))
            obs = row.get('Observaciones', '').strip()
            
            loaded_rows += 1
            reg_id = loaded_rows
            
            registros_sql.append(
                f"({reg_id}, '{fecha}', {id_maquina}, {id_turno}, "
                f"{sql_str(pseudo) if pseudo else 'NULL'}, "
                f"{sql_num(id_ref)}, "
                f"{sql_num(horas_trab)}, NULL, {sql_num(pacas)}, {sql_num(horas_no_trab)}, "
                f"{sql_num(id_tp)}, "
                f"{sql_str(obs_paro) if obs_paro and obs_paro != 'No aplica' else 'NULL'}, "
                f"{sql_num(tiempo_paro)}, "
                f"{sql_str(obs) if obs else 'NULL'})"
            )
            
            # Extraer detalles de paro (códigos 1-18)
            for n in range(1, 19):
                col_name = f'Codigo de paro {n}'
                val = safe_decimal(row.get(col_name))
                if val is not None and val > 0:
                    detalles_paro_sql.append(f"({reg_id}, {n}, {val})")
    
    # ---- Escribir archivo de operarios ----
    print(f"Generando SQL de operarios ({len(operarios_map)} encontrados)...")
    with open(os.path.join(OUTPUT_DIR, '04_datos_operarios.sql'), 'w', encoding='utf-8') as f:
        f.write("-- Operarios pseudonimizados (generado automáticamente)\n")
        f.write("-- NO contiene nombres reales\n")
        f.write("USE paros_produccion;\n\n")
        for name, pseudo in operarios_map.items():
            f.write(f"INSERT INTO operario (pseudonimo) VALUES ('{pseudo}');\n")
    
    # ---- Escribir archivo de referencias ----
    print(f"Generando SQL de referencias ({len(referencias)} encontradas)...")
    with open(os.path.join(OUTPUT_DIR, '05_datos_referencias.sql'), 'w', encoding='utf-8') as f:
        f.write("-- Catálogo de referencias/productos\n")
        f.write("USE paros_produccion;\n\n")
        for name, rid in referencias.items():
            safe_name = name.replace("'", "''")
            f.write(f"INSERT INTO referencia (nombre) VALUES ('{safe_name}');\n")
    
    # ---- Escribir registros de producción ----
    print(f"Generando SQL de registros ({loaded_rows} registros)...")
    with open(os.path.join(OUTPUT_DIR, '06_datos_registros.sql'), 'w', encoding='utf-8') as f:
        f.write("-- Registros de producción migrados del Excel\n")
        f.write("-- Datos pseudonimizados\n")
        f.write("USE paros_produccion;\n\n")
        f.write("-- Desactivar FK temporalmente para carga masiva\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
        
        # Insertar en lotes de 500
        batch_size = 500
        f.write("INSERT INTO registro_produccion\n")
        f.write("(id_registro, fecha, id_maquina, id_turno, id_operario, id_referencia,\n")
        f.write(" horas_trabajadas, meta_por_hora, pacas_producidas, horas_no_trabajadas,\n")
        f.write(" id_tipo_paro, observaciones_paro, tiempo_paro_minutos, observaciones)\n")
        f.write("VALUES\n")
        
        # Reemplazar pseudónimos por IDs de operario
        # Los IDs se asignan en orden de inserción
        op_id_map = {}
        for i, (name, pseudo) in enumerate(operarios_map.items(), 1):
            op_id_map[pseudo] = i
        
        # Reescribir con IDs correctos
        final_regs = []
        for reg in registros_sql:
            # Reemplazar pseudo por id_operario
            for pseudo, oid in op_id_map.items():
                reg = reg.replace(f"'{pseudo}'", str(oid))
            final_regs.append(reg)
        
        for i, reg in enumerate(final_regs):
            sep = ',' if i < len(final_regs) - 1 else ';'
            f.write(f"{reg}{sep}\n")
            if (i + 1) % batch_size == 0 and i < len(final_regs) - 1:
                f.write(";\n\nINSERT INTO registro_produccion\n")
                f.write("(id_registro, fecha, id_maquina, id_turno, id_operario, id_referencia,\n")
                f.write(" horas_trabajadas, meta_por_hora, pacas_producidas, horas_no_trabajadas,\n")
                f.write(" id_tipo_paro, observaciones_paro, tiempo_paro_minutos, observaciones)\n")
                f.write("VALUES\n")
        
        f.write("\nSET FOREIGN_KEY_CHECKS = 1;\n")
    
    # ---- Escribir detalles de paro ----
    print(f"Generando SQL de detalles de paro ({len(detalles_paro_sql)} registros)...")
    with open(os.path.join(OUTPUT_DIR, '07_datos_detalles_paro.sql'), 'w', encoding='utf-8') as f:
        f.write("-- Detalles de paro por código migrados del Excel\n")
        f.write("USE paros_produccion;\n\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
        
        f.write("INSERT INTO detalle_paro (id_registro, id_codigo, duracion_minutos)\nVALUES\n")
        for i, dp in enumerate(detalles_paro_sql):
            sep = ',' if i < len(detalles_paro_sql) - 1 else ';'
            f.write(f"{dp}{sep}\n")
            if (i + 1) % 1000 == 0 and i < len(detalles_paro_sql) - 1:
                f.write(";\n\nINSERT INTO detalle_paro (id_registro, id_codigo, duracion_minutos)\nVALUES\n")
        
        f.write("\nSET FOREIGN_KEY_CHECKS = 1;\n")
    
    # ---- Mapeo de pseudonimización (PRIVADO - NO subir a GitHub) ----
    with open(os.path.join(BASE, 'migration', 'scripts', 'MAPEO_PRIVADO_NO_PUBLICAR.csv'), 'w', encoding='utf-8') as f:
        f.write("tipo,nombre_real,pseudonimo\n")
        for name, pseudo in operarios_map.items():
            f.write(f"operario,{name},{pseudo}\n")
        for name, pseudo in personal_map.items():
            f.write(f"personal_mto,{name},{pseudo}\n")
    
    # ---- Reporte de migración ----
    print("\n" + "="*60)
    print("REPORTE DE MIGRACIÓN")
    print("="*60)
    print(f"Total filas en CSV:       {total_rows}")
    print(f"Registros cargados:       {loaded_rows}")
    print(f"Registros rechazados:     {rejected_rows}")
    print(f"Detalles de paro:         {len(detalles_paro_sql)}")
    print(f"Operarios únicos:         {len(operarios_map)}")
    print(f"Referencias únicas:       {len(referencias)}")
    print(f"Tipos de paro únicos:     {len(tipos_paro)}")
    print(f"\nArchivos generados:")
    print(f"  - sql/04_datos_operarios.sql")
    print(f"  - sql/05_datos_referencias.sql")
    print(f"  - sql/06_datos_registros.sql")
    print(f"  - sql/07_datos_detalles_paro.sql")
    print(f"  - migration/scripts/MAPEO_PRIVADO_NO_PUBLICAR.csv (NO publicar)")
    
    if rejected_rows > 0:
        print(f"\nRazones de rechazo (primeras 20):")
        for r in rejected_reasons[:20]:
            print(f"  - {r}")
    
    # Guardar reporte
    with open(os.path.join(BASE, 'docs', '06_VALIDACION_MIGRACION.md'), 'w', encoding='utf-8') as f:
        f.write("# 06 — Validación de la Migración\n\n")
        f.write("## Resumen cuantitativo\n\n")
        f.write(f"| Métrica | Valor |\n")
        f.write(f"|---------|-------|\n")
        f.write(f"| Total filas origen (CSV) | {total_rows} |\n")
        f.write(f"| Registros procesados | {total_rows} |\n")
        f.write(f"| Registros cargados exitosamente | {loaded_rows} |\n")
        f.write(f"| Registros rechazados | {rejected_rows} |\n")
        f.write(f"| Detalles de paro generados | {len(detalles_paro_sql)} |\n")
        f.write(f"| Operarios únicos identificados | {len(operarios_map)} |\n")
        f.write(f"| Referencias únicas | {len(referencias)} |\n")
        f.write(f"| Tipos de paro únicos | {len(tipos_paro)} |\n")
        f.write(f"\n## Pseudonimización\n\n")
        f.write(f"- Se asignaron pseudónimos OP-001 a OP-{op_counter[0]:03d} a los operarios\n")
        f.write(f"- El mapeo real→pseudónimo se almacena en `migration/scripts/MAPEO_PRIVADO_NO_PUBLICAR.csv`\n")
        f.write(f"- Este archivo **NO debe subirse** al repositorio público\n")
        if rejected_rows > 0:
            f.write(f"\n## Registros rechazados\n\n")
            for r in rejected_reasons:
                f.write(f"- {r}\n")

if __name__ == '__main__':
    main()

