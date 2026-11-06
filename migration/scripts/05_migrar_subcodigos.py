"""
05_migrar_subcodigos.py
Migra la tabla de subcódigos del Excel a sentencias SQL INSERT
para la tabla detalle_subcodigo.
"""
import csv
import os
from collections import OrderedDict

BASE = r"c:\Users\Sebas\Desktop\Bases datos 1\TRABAJO2"
CSV_DIR = os.path.join(BASE, "insumos_originales", "02_EXTRACCION_EXCEL")
SUB_CSV = os.path.join(CSV_DIR, "BASE_DATOS_SUBCODIGOS.csv")
OUTPUT = os.path.join(BASE, "sql", "07b_datos_subcodigos.sql")

# Mapeo de máquinas
maquinas = {'Vinilos_1': 1, 'Vinilos_2': 2, 'Vinilos_3': 3, 'Vinilos_4': 4}
turnos = {
    '6am-2pm (Turno 1)': 1, '2pm-10pm (Turno 2)': 2, '10pm-6am (Turno 3)': 3,
    '6am-4:30pm': 4, '6am-6pm': 5, '6pm-6am': 6, 'No aplica': 7
}

# Mapeo de textos de subcódigo al id_subcodigo del catálogo (02_datos_catalogos.sql)
# Los IDs se asignan por AUTO_INCREMENT en orden de inserción
subcod_text_to_id = {}

def build_subcod_map():
    # Código 01: 31 subcódigos, IDs 1-31
    sub01 = [
        '1.1 Sistema alimentador de envases', '1.1 SISTEMA ALIMENTADOR DE ENVASES',
        '1.1.A Banda', '1.1.B Motor', '1.1.B  Motor',
        '1.1.C Sensor', '1.1.C  Sensor',
        '1.2 Sistema de dosificación', '1.2 SISTEMA DE DOSIFICACIÓN',
        '1.2.A Cambio de racores', '1.2.B Ajuste de sensor',
        '1.2.C Cambio de Valvula', '1.2.C Cambio de valvula', '1.2.C Cambio de válvula',
        '1.2.D Retenedores', "1.2.E O'Ring", "1.2.E O'ring",
        '1.3 Sistema de banda de entrada', '1.3.A Banda', '1.3.B Motor',
        '1.4 Sistema de tapado', '1.4.A Motor del transfer',
        '1.4.B Pisador de tapa', '1.4.3 Sensor',
        '1.5 Sistema de alimentación de tapa', '1.5 SISTEMA DE ALIMENTACIÓN DE TAPA',
        '1.5.A Banda', '1.5.B Motor', '1.5.C Sensor',
        '1.6 Sistema Video Jet', '1.6 SISTEMA VIDEO JET',
        '1.6.A Fotocelda', '1.6.B Sensor', '1.6.E Sensor',
        '1.7 Sistema de sujeción y roscadores',
        '1.7.A Banda de sujeción', '1.7.B Roscadores',
        '1.8 Sistema etiquetadora', '1.8.A Banda', '1.8.B Motor', '1.8.C Sensor',
    ]
    # Map by prefix
    id_map = {
        '1.1 ': 1, '1.1.A': 2, '1.1.B': 3, '1.1.C': 4,
        '1.2 ': 5, '1.2.A': 6, '1.2.B': 7, '1.2.C': 8, '1.2.D': 9, '1.2.E': 10,
        '1.3 ': 11, '1.3.A': 12, '1.3.B': 13,
        '1.4 ': 14, '1.4.A': 15, '1.4.B': 16, '1.4.3': 17,
        '1.5 ': 18, '1.5.A': 19, '1.5.B': 20, '1.5.C': 21,
        '1.6 ': 22, '1.6.A': 23, '1.6.B': 24, '1.6.E': 24,
        '1.7 ': 25, '1.7.A': 26, '1.7.B': 27,
        '1.8 ': 28, '1.8.A': 29, '1.8.B': 30, '1.8.C': 31,
        # Código 03: IDs 32-36
        '3.1': 32, '3.2': 33, '3.3': 34, '3.4': 35, '3.5': 36,
        # Código 05: IDs 37-47
        '5.1 ': 37, '5.1': 37,
        '5.2 ': 38, '5.2': 38,
        '5.3 ': 39, '5.3': 39,
        '5.4 ': 40, '5.4': 40,
        '5.5 ': 41, '5.5': 41,
        '5.6 ': 42, '5.6': 42,
        '5.7 ': 43, '5.7': 43,
        '5.8 ': 44, '5.8': 44,
        '5.9 ': 45, '5.9': 45,
        '5.10': 46,
        '5.11': 47,
    }
    return id_map

def find_subcod_id(text, id_map):
    if not text or text.strip() in ('', ' '):
        return None
    text = text.strip()
    # Try exact prefix matches (longest first)
    for prefix_len in [5, 4, 3]:
        if len(text) >= prefix_len:
            prefix = text[:prefix_len]
            if prefix in id_map:
                return id_map[prefix]
    # Try shorter
    for prefix in sorted(id_map.keys(), key=len, reverse=True):
        if text.startswith(prefix) or text.lower().startswith(prefix.lower()):
            return id_map[prefix]
    return None

def safe_decimal(val):
    if val is None or str(val).strip() in ('', ' '):
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

def sql_str(val):
    if val is None:
        return 'NULL'
    val = str(val).replace("'", "''").replace("\\", "\\\\")
    return f"'{val}'"

def main():
    id_map = build_subcod_map()
    
    # Leer el mapeo de operarios del archivo privado
    op_map_file = os.path.join(BASE, 'migration', 'scripts', 'MAPEO_PRIVADO_NO_PUBLICAR.csv')
    op_name_to_id = {}
    with open(op_map_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        op_idx = 0
        for row in reader:
            if row['tipo'] == 'operario':
                op_idx += 1
                op_name_to_id[row['nombre_real']] = op_idx
    
    # Necesitamos buscar el id_registro correspondiente por (fecha, maquina, turno, operario)
    # Primero cargamos la tabla principal de CSV para construir un índice
    main_csv = os.path.join(CSV_DIR, "BASE_DATOS_T_BASEDATOS.csv")
    reg_index = {}  # (fecha, maquina, turno, operario) -> id_registro
    with open(main_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            fecha = row.get('Fecha', '').strip()
            maquina = row.get('Maquina', '').strip()
            turno = row.get('Turno', '').strip() or 'No aplica'
            operario = row.get('Operario', '').strip()
            key = (fecha, maquina, turno, operario)
            if key not in reg_index:
                reg_index[key] = i
    
    # Leer subcódigos
    inserts = []
    total = 0
    matched = 0
    unmatched_regs = 0
    unmatched_subcods = []
    
    with open(SUB_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            fecha = row.get('Fecha', '').strip()
            maquina = row.get('Maquina', '').strip()
            turno = row.get('Turno', '').strip() or 'No aplica'
            operario = row.get('Operario', '').strip()
            
            key = (fecha, maquina, turno, operario)
            id_registro = reg_index.get(key)
            if id_registro is None:
                unmatched_regs += 1
                continue
            
            # Subcódigo 1
            subcod1_text = row.get('Subcodigo 1', '').strip()
            subcod1_min = safe_decimal(row.get('Codigo de paro 1'))
            if subcod1_text and subcod1_text not in ('', ' '):
                sid = find_subcod_id(subcod1_text, id_map)
                if sid:
                    dur = subcod1_min if subcod1_min else 0
                    inserts.append(f"({id_registro}, {sid}, {dur}, NULL, NULL)")
                    matched += 1
                else:
                    unmatched_subcods.append(f"Cod01: '{subcod1_text}'")
            
            # Subcódigo 3
            subcod3_text = row.get('Subcodigo 3', '').strip()
            subcod3_min = safe_decimal(row.get('Codigo de paro 3'))
            if subcod3_text and subcod3_text not in ('', ' '):
                sid = find_subcod_id(subcod3_text, id_map)
                if sid:
                    dur = subcod3_min if subcod3_min else 0
                    inserts.append(f"({id_registro}, {sid}, {dur}, NULL, NULL)")
                    matched += 1
                else:
                    unmatched_subcods.append(f"Cod03: '{subcod3_text}'")
            
            # Subcódigo 5
            subcod5_text = row.get('Subcodigo 5', '').strip()
            subcod5_min = safe_decimal(row.get('Codigo de paro 5'))
            area = row.get('Área involucrada en subcodigo 5', '').strip()
            personal = row.get('Personal involucrado', '').strip()
            if subcod5_text and subcod5_text not in ('', ' '):
                sid = find_subcod_id(subcod5_text, id_map)
                if sid:
                    dur = subcod5_min if subcod5_min else 0
                    area_sql = sql_str(area) if area and area not in ('', ' ') else 'NULL'
                    # Pseudonimizar personal
                    if personal and personal.strip() not in ('', ' ', 'No aplica'):
                        pers_sql = sql_str('PM-ANON')  # pseudonimizado
                    else:
                        pers_sql = 'NULL'
                    inserts.append(f"({id_registro}, {sid}, {dur}, {area_sql}, {pers_sql})")
                    matched += 1
                else:
                    unmatched_subcods.append(f"Cod05: '{subcod5_text}'")
    
    # Escribir SQL
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write("-- Detalles de subcódigos migrados de la tabla Base_de_datos_subcodigos\n")
        f.write("-- Datos pseudonimizados\n")
        f.write("USE paros_produccion;\n\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
        
        if inserts:
            f.write("INSERT INTO detalle_subcodigo (id_registro, id_subcodigo, duracion_minutos, area_involucrada, personal_involucrado)\nVALUES\n")
            for i, ins in enumerate(inserts):
                sep = ',' if i < len(inserts) - 1 else ';'
                f.write(f"{ins}{sep}\n")
        
        f.write("\nSET FOREIGN_KEY_CHECKS = 1;\n")
    
    print(f"Total filas subcódigos CSV: {total}")
    print(f"Subcódigos migrados: {matched}")
    print(f"Registros padre no encontrados: {unmatched_regs}")
    print(f"Subcódigos no mapeados: {len(set(unmatched_subcods))}")
    if unmatched_subcods:
        for u in sorted(set(unmatched_subcods))[:15]:
            print(f"  - {u}")
    print(f"\nArchivo generado: {OUTPUT}")

if __name__ == '__main__':
    main()

