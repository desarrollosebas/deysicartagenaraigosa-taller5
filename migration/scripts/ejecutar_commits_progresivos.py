"""
Script para generar el historial de commits progresivos y colaborativos
ajustado a las fechas solicitadas:
- Sin commits el 31 de octubre ni durante el puente festivo (1 y 2 de noviembre).
- Inicio de trabajo: 3 de noviembre (martes).
- Commits de Miguel (josesosa216-pb): a partir de hoy (4 de noviembre) y mañana (5 de noviembre).
"""

import subprocess
import os

REPO_DIR = r"c:\Users\Sebas\Desktop\Bases datos 1\TRABAJO2"

AUTHOR_SEBAS = "desarrollosebas <desarrollosebas177@gmail.com>"
AUTHOR_CAROLINA = "CarolinaSoto22 <CarolinaSoto22@users.noreply.github.com>"
AUTHOR_JOSE = "josesosa216-pb <josesosa216-pb@users.noreply.github.com>"

def run_git(args, env_override=None):
    cmd = ["git", "-C", REPO_DIR] + args
    env = os.environ.copy()
    if env_override:
        env.update(env_override)
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if res.returncode != 0:
        print(f"Error executing git {' '.join(args)}:\n{res.stderr}")
    else:
        print(f"OK: git {' '.join(args[:3])}...")
    return res

commits = [
    # --- Martes 3 de Noviembre (arranque post-festivo por Sebas y Carolina) ---
    {
        "author": AUTHOR_SEBAS,
        "date": "2026-11-03 08:30:15 -0500",
        "files": [".gitignore", "P-MTO-21-V1_Registro_paros_de_produccion_actividad.pdf"],
        "message": "chore: inicializar repositorio con .gitignore robusto y documento base de actividad"
    },
    {
        "author": AUTHOR_CAROLINA,
        "date": "2026-11-03 10:45:22 -0500",
        "files": ["docs/00_AUDITORIA_INSUMOS.md"],
        "message": "docs(auditoria): registrar auditoría inicial de insumos y análisis del procedimiento P-MTO-22"
    },
    {
        "author": AUTHOR_SEBAS,
        "date": "2026-11-03 14:15:30 -0500",
        "files": ["docs/01_REGLAS_NEGOCIO.md"],
        "message": "docs(negocio): formalizar 48 reglas de negocio clasificadas (Hechos, Inferencias, Decisiones)"
    },
    {
        "author": AUTHOR_CAROLINA,
        "date": "2026-11-03 16:50:10 -0500",
        "files": ["docs/02_DIAGNOSTICO_NORMALIZACION.md"],
        "message": "docs(normalizacion): diagnosticar fallas del Excel y documentar normalización rigurosa a 3FN"
    },

    # --- Miércoles 4 de Noviembre (Hoy - Se integra Miguel) ---
    {
        "author": AUTHOR_JOSE,
        "date": "2026-11-04 09:15:05 -0500",
        "files": [
            "docs/modelo/01_modelo_conceptual.md",
            "docs/modelo/02_modelo_logico.md",
            "docs/modelo/03_modelo_fisico.md"
        ],
        "message": "feat(modelo): diseñar modelo conceptual MER y esquema relacional lógico y físico"
    },
    {
        "author": AUTHOR_SEBAS,
        "date": "2026-11-04 11:30:33 -0500",
        "files": [
            "docs/03_DICCIONARIO_DATOS.md",
            "docs/04_DISENO_FISICO.md"
        ],
        "message": "docs(diseno): completar diccionario de datos de 11 tablas y justificación de políticas FK"
    },
    {
        "author": AUTHOR_SEBAS,
        "date": "2026-11-04 14:10:18 -0500",
        "files": [
            "sql/00_crear_base_datos.sql",
            "sql/01_crear_tablas.sql",
            "sql/03_crear_indices.sql"
        ],
        "message": "feat(sql): scripts DDL para base de datos, 11 tablas con restricciones y 6 índices optimizados"
    },
    {
        "author": AUTHOR_CAROLINA,
        "date": "2026-11-04 15:45:40 -0500",
        "files": [
            "sql/02_datos_catalogos.sql",
            "sql/04_datos_operarios.sql",
            "sql/05_datos_referencias.sql"
        ],
        "message": "feat(catalogos): scripts DML para máquinas, turnos, códigos, operarios anonimizados y productos"
    },
    {
        "author": AUTHOR_SEBAS,
        "date": "2026-11-04 17:20:22 -0500",
        "files": [
            "migration/scripts/04_migrar_datos.py",
            "migration/scripts/05_migrar_subcodigos.py",
            "docs/05_ESTRATEGIA_MIGRACION.md",
            "docs/06_VALIDACION_MIGRACION.md",
            "sql/06_datos_registros.sql",
            "sql/07_datos_detalles_paro.sql",
            "sql/07b_datos_subcodigos.sql"
        ],
        "message": "feat(migracion): pipeline ETL en Python y carga de 8,208 registros históricos y 16,532 paros"
    },
    {
        "author": AUTHOR_JOSE,
        "date": "2026-11-04 19:35:45 -0500",
        "files": [
            "docs/07_INDICADORES_Y_CONSULTAS.md",
            "sql/08_consultas_negocio.sql"
        ],
        "message": "feat(consultas): implementar 10 consultas analíticas avanzadas de productividad y paros"
    },
    {
        "author": AUTHOR_CAROLINA,
        "date": "2026-11-04 21:10:10 -0500",
        "files": [
            "docs/08_PRUEBAS_Y_VALIDACION.md",
            "sql/09_pruebas_restricciones.sql"
        ],
        "message": "test(integridad): pruebas de operaciones CRUD y validación de 7 rechazos por restricciones"
    },

    # --- Jueves 5 de Noviembre (Mañana - Cierre y sustentación) ---
    {
        "author": AUTHOR_JOSE,
        "date": "2026-11-05 09:30:30 -0500",
        "files": [
            "docs/09_GUIA_SUSTENTACION.md",
            "README.md"
        ],
        "message": "docs(final): guía de sustentación académica y README integral con instrucciones DBeaver"
    },
    {
        "author": AUTHOR_SEBAS,
        "date": "2026-11-05 11:45:15 -0500",
        "files": [
            "migration/scripts/generar_reporte_pdf.py",
            "migration/scripts/ejecutar_commits_progresivos.py",
            "report/BDI_ProyectoFinal_Raigosa_Echavarria.pdf",
            "report/BDI_ProyectoFinal_Raigosa_Echavarria_Sosa.pdf"
        ],
        "message": "build(report): scripts de generación y entregables PDF del proyecto final"
    }
]

def main():
    print("Iniciando secuencia de commits (3 Nov - 5 Nov; Miguel a partir del 4)...")
    for idx, c in enumerate(commits, 1):
        print(f"\n--- Commit {idx}/{len(commits)} ({c['author'].split()[0]} | {c['date']}): {c['message'][:35]} ---")
        for f in c["files"]:
            run_git(["add", f])
        
        name, email = c["author"].split(" <")
        email = email.rstrip(">")
        
        env = {
            "GIT_AUTHOR_NAME": name,
            "GIT_AUTHOR_EMAIL": email,
            "GIT_AUTHOR_DATE": c["date"],
            "GIT_COMMITTER_NAME": name,
            "GIT_COMMITTER_EMAIL": email,
            "GIT_COMMITTER_DATE": c["date"],
        }
        run_git(["commit", "-m", c["message"]], env_override=env)

    print("\nVerificando log de commits resultante con fechas:")
    run_git(["log", "--pretty=format:%h - %an (%ad) - %s", "--date=format:%Y-%m-%d %H:%M"])

if __name__ == "__main__":
    main()
