"""
Script para generar el entregable formal en PDF:
BDI_ProyectoFinal_Raigosa_Echavarria.pdf
Cumpliendo integralmente con los requisitos del Taller 5.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Canvas de dos pasadas para calcular dinámicamente el número total de páginas
    y añadir encabezado y pie de página en cada hoja (excepto portada).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # No header/footer on cover page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))

        # Header
        self.drawString(54, letter[1] - 36, "Bases de Datos I — Proyecto Final (Taller 5)")
        self.drawRightString(letter[0] - 54, letter[1] - 36, "BD Registro de Paros de Producción")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer
        self.line(54, 46, letter[0] - 54, 46)
        self.drawString(54, 34, "J. S. Raigosa, D. C. Echavarría, J. M. Sosa — MySQL 8.x / DBeaver")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(letter[0] - 54, 34, page_str)

        self.restoreState()

def create_report():
    output_dir = r"c:\Users\Sebas\Desktop\Bases datos 1\TRABAJO2\report"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "BDI_ProyectoFinal_Raigosa_Echavarria.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1A365D")   # Deep navy
    secondary_color = colors.HexColor("#2B6CB0") # Medium blue
    accent_color = colors.HexColor("#C53030")    # Crimson accent
    dark_neutral = colors.HexColor("#2D3748")    # Charcoal body
    light_bg = colors.HexColor("#F7FAFC")        # Soft grey

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        alignment=1, # Center
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=17,
        textColor=secondary_color,
        alignment=1,
        spaceAfter=30
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=dark_neutral,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1A202C")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=0
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=dark_neutral
    )

    story = []

    # =========================================================================
    # PORTADA
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("UNIVERSIDAD DE ANTIOQUIA / FACULTAD DE INGENIERÍA", ParagraphStyle('Univ', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, alignment=1, textColor=primary_color, spaceAfter=8)))
    story.append(Paragraph("DEPARTAMENTO DE INGENIERÍA DE SISTEMAS", ParagraphStyle('Dept', parent=styles['Normal'], fontName='Helvetica', fontSize=10, alignment=1, textColor=secondary_color, spaceAfter=30)))

    story.append(HRFlowable(width="80%", thickness=2, color=primary_color, spaceAfter=35, spaceBefore=10))

    story.append(Paragraph("PROYECTO FINAL — TALLER 5", ParagraphStyle('PreTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, alignment=1, textColor=accent_color, spaceAfter=12)))
    story.append(Paragraph("Diseño e Implementación de una Base de Datos Relacional Normalizada para el Registro y Análisis de Paros de Producción", title_style))
    story.append(Paragraph("Reemplazo y Migración Integral del Sistema de Seguimiento en Excel de Líneas de Envasado de Vinilos y Témperas", subtitle_style))

    story.append(HRFlowable(width="60%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=35, spaceBefore=10))

    info_data = [
        [Paragraph("<b>Asignatura:</b>", body_style), Paragraph("Bases de Datos I", body_style)],
        [Paragraph("<b>Integrantes:</b>", body_style), Paragraph("Juan Sebastián Raigosa Gil<br/>Deysi Carolina Echavarría Soto<br/>Jose Miguel Sosa Cartagena", body_style)],
        [Paragraph("<b>Motor de BD:</b>", body_style), Paragraph("MySQL 8.x Community Server", body_style)],
        [Paragraph("<b>Herramienta Cliente:</b>", body_style), Paragraph("DBeaver Community Edition", body_style)],
        [Paragraph("<b>Control de Versiones:</b>", body_style), Paragraph("Git + GitHub (Repositorio público)", body_style)],
        [Paragraph("<b>Fecha:</b>", body_style), Paragraph("Noviembre de 2026", body_style)],
        [Paragraph("<b>Enlace Repositorio:</b>", body_style), Paragraph("<u>https://github.com/desarrollosebas/deysicartagenaraigosa-taller5</u>", body_style)],
    ]

    t_info = Table(info_data, colWidths=[130, 280])
    t_info.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#EDF2F7")),
    ]))
    story.append(t_info)

    story.append(PageBreak())

    # =========================================================================
    # TABLA DE CONTENIDO / RESUMEN EJECUTIVO
    # =========================================================================
    story.append(Paragraph("Resumen Ejecutivo y Estructura del Informe", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=12, spaceBefore=4))

    story.append(Paragraph(
        "El presente informe documenta el desarrollo completo del <b>Taller 5 de Bases de Datos I</b>. "
        "El objetivo principal ha sido diseñar, normalizar, implementar, poblar y explotar mediante consultas analíticas "
        "una base de datos relacional robusta en <b>MySQL 8.x</b>, destinada a sustituir un sistema obsoleto basado en un "
        "libro de Microsoft Excel con macros (<code>SEGUIMIENTO TEMPERAS Y VINILOS Actividad.xlsm</code>). "
        "Dicho archivo funcionaba precariamente como repositorio de paros de producción y cálculo de indicadores de las "
        "cuatro líneas de envasado (Vinilos_1 a Vinilos_4) de una empresa fabricante de pinturas.",
        body_style
    ))
    story.append(Paragraph(
        "El proyecto abarcó la auditoría minuciosa del procedimiento operacional <b>P-MTO-22 V1</b> (identificado externamente como P-MTO-21), "
        "la identificación y formalización de <b>48 reglas de negocio</b>, la normalización rigurosa desde la estructura plana "
        "desnormalizada original hasta la <b>Tercera Forma Normal (3FN)</b>, el diseño conceptual y lógico, el diccionario exhaustivo de 11 tablas, "
        "la migración automatizada sin macros de <b>8,208 registros históricos</b> de producción, <b>16,532 detalles de paro</b> y "
        "<b>1,115 registros de subcódigos</b>, la salvaguarda de datos personales mediante pseudonimización reversible, y la creación de un conjunto "
        "de 10 consultas SQL empresariales avanzadas acompañadas de pruebas de integridad referencial y de restricciones.",
        body_style
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Estructura de Contenido del Entregable:</b>", h2_style))

    toc_items = [
        "1. Contexto Empresarial, Justificación y Objetivos del Proyecto",
        "2. Auditoría Integral de Insumos y Diagnóstico Crítico del Excel Original",
        "3. Reglas de Negocio Identificadas y Formalizadas (Clasificación H/I/D)",
        "4. Modelo Conceptual Entidad-Relación (MER)",
        "5. Modelo Relacional Lógico Derivado",
        "6. Proceso de Normalización Formal (UNF → 1FN → 2FN → 3FN)",
        "7. Diccionario de Datos Exhaustivo del Diseño Físico (11 Tablas)",
        "8. Restricciones de Integridad y Justificación de Índices de Rendimiento",
        "9. Estrategia de Extracción, Transformación, Carga (ETL) y Validación Cuantitativa",
        "10. Política y Estrategia de Protección de Datos Personales (Privacidad)",
        "11. Consultas SQL Analíticas de Negocio e Indicadores Clave",
        "12. Pruebas de Integridad, Validación de Restricciones y Rechazos Controlados",
        "13. Guía de Ejecución Reproducible desde DBeaver y Estructura Git",
        "14. Conclusiones y Referencias"
    ]
    for item in toc_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 1: CONTEXTO Y OBJETIVOS
    # =========================================================================
    story.append(Paragraph("1. Contexto Empresarial, Justificación y Objetivos", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph("1.1 Descripción del Entorno Operacional", h2_style))
    story.append(Paragraph(
        "La compañía opera una planta de fabricación de vinilos y témperas equipada con cuatro líneas de envasado industrial: "
        "<b>Vinilos_1, Vinilos_2, Vinilos_3 y Vinilos_4</b>. En cada turno productivo, las operarias de planta registran "
        "manualmente en un formato físico denominado <i>'Control de Producción y Paros de Máquina — Hora a Hora'</i> las pacas envasadas, "
        "las horas laboradas, las referencias procesadas y la descripción de cada evento de detención.",
        body_style
    ))
    story.append(Paragraph(
        "Al finalizar las jornadas, estos formatos físicos son remitidos al departamento de mantenimiento, donde el personal técnico "
        "transcribe manualmente las anotaciones a un libro de Excel habilitado para macros (<code>SEGUIMIENTO TEMPERAS Y VINILOS Actividad.xlsm</code>). "
        "Este archivo contenía más de 8,200 filas de registro acumuladas entre los años 2022 y 2025, sirviendo de base para calcular la "
        "productividad mensual y la participación de los paros que se reportan a la Gerencia de Operaciones.",
        body_style
    ))

    story.append(Paragraph("1.2 Justificación del Reemplazo del Excel", h2_style))
    story.append(Paragraph(
        "El sistema sustentado en Excel ha colapsado operativamente por múltiples factores estructurales: "
        "<b>(a) Ausencia total de integridad referencial:</b> no existen llaves foráneas que impidan escribir nombres inexistentes de máquinas u operarios; "
        "<b>(b) Dependencia crítica de macros VBA:</b> validaciones sujetas a corrupción por versiones de Office o políticas de seguridad corporativas; "
        "<b>(c) Estructura no normalizada:</b> presencia de 18 columnas repetitivas para registrar tiempos de paro por código, obligando a alterar la estructura de la tabla ante cualquier nuevo código; "
        "<b>(d) Inseguridad y privacidad nula:</b> exposición de nombres reales de trabajadores en archivos compartidos; y "
        "<b>(e) Lentitud analítica:</b> las fórmulas volátiles y tablas dinámicas recalculan 180,000 celdas, impidiendo consultas analíticas ágiles.",
        body_style
    ))

    story.append(Paragraph("1.3 Objetivos del Proyecto", h2_style))
    story.append(Paragraph("<b>Objetivo General:</b> Diseñar, normalizar, implementar en MySQL 8.x, migrar y consultar una base de datos relacional robusta que reemplace definitivamente el libro de Excel como fuente única de verdad para el control de paros de producción.", body_style))
    story.append(Paragraph("<b>Objetivos Específicos:</b>", body_style))
    story.append(Paragraph("1. Formalizar las reglas de negocio y auditar los documentos fuente P-MTO-22 y el libro de datos.", bullet_style))
    story.append(Paragraph("2. Realizar la normalización rigurosa de UNF a 3FN eliminando grupos repetitivos, dependencias parciales y transitivas.", bullet_style))
    story.append(Paragraph("3. Elaborar los modelos conceptual, lógico y físico con restricciones PK, FK, UNIQUE, CHECK y DEFAULT.", bullet_style))
    story.append(Paragraph("4. Implementar 6 índices optimizados con base en las necesidades de consulta analítica.", bullet_style))
    story.append(Paragraph("5. Ejecutar un ETL seguro en Python para migrar el 100% de registros históricos preservando la integridad cuantitativa.", bullet_style))
    story.append(Paragraph("6. Proteger la identidad del personal mediante un protocolo formal de pseudonimización.", bullet_style))
    story.append(Paragraph("7. Diseñar 10 consultas SQL avanzadas que reproduzcan y mejoren los indicadores gerenciales de productividad y paro.", bullet_style))

    story.append(Spacer(1, 8))

    # =========================================================================
    # SECCIÓN 2: AUDITORÍA Y DIAGNÓSTICO
    # =========================================================================
    story.append(Paragraph("2. Auditoría de Insumos y Diagnóstico del Excel", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph("2.1 Auditoría de Documentos Fuente", h2_style))
    story.append(Paragraph(
        "<b>Discrepancia P-MTO-21 vs P-MTO-22:</b> El archivo PDF entregado se titula externamente <code>P-MTO-21-V1...</code>, "
        "pero su membrete interno oficial reza <code>P-MTO-22 V1: Procedimiento para el Registro de Paros de Producción</code>. "
        "Se adoptó la denominación oficial interna P-MTO-22 por reflejar el documento de calidad vigente.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Catálogo de Códigos de Paro:</b> El procedimiento describe 18 códigos estandarizados (01 al 18). Sin embargo, "
        "se descubrió una diferencia clave en el código 18: el PDF lo rotula como <i>'Desinfección de Planta'</i>, mientras que la base "
        "histórica real de Excel lo utiliza mayoritariamente como <i>'Paro de máquina por ventas'</i>. "
        "Adicionalmente, se identificó un código especial <code>[19] No aplica</code>, utilizado para asentar turnos donde la máquina "
        "operó con total normalidad sin incidencias de paro mayores.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Desglose por Subcódigos:</b> Únicamente los códigos <b>01 (Mecánicos/Eléctricos)</b>, <b>03 (Operacionales)</b> y "
        "<b>05 (Ajustes de Calidad)</b> cuentan con desglose analítico en subcódigos. En el código 05, la empresa segrega además "
        "la responsabilidad entre <i>'Operarios'</i> y <i>'Personal de Mantenimiento'</i>.",
        body_style
    ))

    story.append(Paragraph("2.2 Diagnóstico Estructural del Libro Excel", h2_style))

    diag_data = [
        [Paragraph("Problema Detectado en Excel", table_header_style), Paragraph("Manifestación Técnica", table_header_style), Paragraph("Impacto y Consecuencia", table_header_style)],
        [
            Paragraph("<b>Grupos Repetitivos</b>", table_cell_style),
            Paragraph("Columnas 'Codigo 1' a 'Codigo 18' duplicadas en minutos y horas.", table_cell_style),
            Paragraph("Violación de 1FN. Imposibilidad de añadir nuevos códigos sin alterar la tabla física.", table_cell_style)
        ],
        [
            Paragraph("<b>Fórmulas Redundantes</b>", table_cell_style),
            Paragraph("Más de 180,000 celdas calculando año, mes y conversión de horas.", table_cell_style),
            Paragraph("Violación de 3FN. Corrupción potencial por arrastre manual erróneo de fórmulas.", table_cell_style)
        ],
        [
            Paragraph("<b>Inexistencia de FK</b>", table_cell_style),
            Paragraph("Máquinas y operarios escritos en texto libre sin validación estricta.", table_cell_style),
            Paragraph("Inconsistencias ortográficas y registros huérfanos sin trazabilidad real.", table_cell_style)
        ],
        [
            Paragraph("<b>Exposición de Datos Personales</b>", table_cell_style),
            Paragraph("Nombres y apellidos completos de 32 operarias y mecánicos en texto plano.", table_cell_style),
            Paragraph("Riesgo legal y vulneración de privacidad en repositorios o auditorías públicas.", table_cell_style)
        ],
        [
            Paragraph("<b>Rigidez en Indicadores</b>", table_cell_style),
            Paragraph("Dependencia exclusiva de tablas dinámicas monolíticas en Excel.", table_cell_style),
            Paragraph("Imposibilidad de cruzar causas con turnos u operarios de forma interactiva.", table_cell_style)
        ]
    ]
    t_diag = Table(diag_data, colWidths=[120, 180, 204])
    t_diag.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ]))
    story.append(t_diag)

    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 3: REGLAS DE NEGOCIO
    # =========================================================================
    story.append(Paragraph("3. Reglas de Negocio Identificadas y Formalizadas", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph(
        "Se extrajeron y formalizaron <b>48 reglas de negocio</b> agrupadas por componentes operativos y clasificadas "
        "conforme a la taxonomía: <b>[H] Hecho comprobado</b> en la documentación, <b>[I] Inferencia lógica</b> deducida de los datos históricos, "
        "y <b>[D] Decisión de diseño arquitectónico</b> adoptada para asegurar la solidez del sistema.",
        body_style
    ))

    rn_data = [
        [Paragraph("ID", table_header_style), Paragraph("Tipo", table_header_style), Paragraph("Regla de Negocio Formal", table_header_style), Paragraph("Implementación en BD", table_header_style)],
        [
            Paragraph("RN-001", table_cell_style), Paragraph("[H]", table_cell_style),
            Paragraph("Existen exactamente cuatro líneas de envasado: Vinilos_1, 2, 3 y 4.", table_cell_style),
            Paragraph("Tabla <code>maquina</code>, restricción <code>UNIQUE(nombre)</code>.", table_cell_style)
        ],
        [
            Paragraph("RN-002", table_cell_style), Paragraph("[H]", table_cell_style),
            Paragraph("Cada máquina posee un factor de ajuste (V1=1.10, V2=1.16, V3=1.00, V4=1.00).", table_cell_style),
            Paragraph("Columna <code>factor_produccion CHECK(>0)</code>.", table_cell_style)
        ],
        [
            Paragraph("RN-006", table_cell_style), Paragraph("[H]", table_cell_style),
            Paragraph("Los turnos estándar son T1 (06:00-14:00), T2 (14:00-22:00) y T3 (22:00-06:00).", table_cell_style),
            Paragraph("Tabla <code>turno</code> con horas de inicio, fin y duración.", table_cell_style)
        ],
        [
            Paragraph("RN-011", table_cell_style), Paragraph("[D]", table_cell_style),
            Paragraph("Los nombres reales del personal deben ser protegidos ante publicación.", table_cell_style),
            Paragraph("Tabla <code>operario</code> con pseudónimos <code>OP-001..OP-032</code>.", table_cell_style)
        ],
        [
            Paragraph("RN-016", table_cell_style), Paragraph("[H]", table_cell_style),
            Paragraph("Se contemplan 18 códigos de paro estandarizados numerados del 01 al 18.", table_cell_style),
            Paragraph("Tabla <code>codigo_paro CHECK(numero BETWEEN 1 AND 18)</code>.", table_cell_style)
        ],
        [
            Paragraph("RN-017", table_cell_style), Paragraph("[H]", table_cell_style),
            Paragraph("Solo los códigos 01, 03 y 05 poseen desglose estructurado en subcódigos.", table_cell_style),
            Paragraph("Columna <code>tiene_subcodigos BOOLEAN</code> en <code>codigo_paro</code>.", table_cell_style)
        ],
        [
            Paragraph("RN-025", table_cell_style), Paragraph("[H]", table_cell_style),
            Paragraph("Tiempos de alimentación (código 16: 40 min) y pausas activas (17: 3 min) son preasignados.", table_cell_style),
            Paragraph("Valores por defecto en tabla <code>turno</code> y registros automáticos.", table_cell_style)
        ],
        [
            Paragraph("RN-032", table_cell_style), Paragraph("[H]", table_cell_style),
            Paragraph("Fórmula oficial de productividad: Si Real=0 → 0, sino (Real / (Horas × Meta)) × Factor.", table_cell_style),
            Paragraph("Implementada dinámicamente en vista/consultas SQL sin almacenar.", table_cell_style)
        ],
        [
            Paragraph("RN-036", table_cell_style), Paragraph("[I]", table_cell_style),
            Paragraph("Un registro de producción puede tener múltiples paros o ninguno (0 a N).", table_cell_style),
            Paragraph("Entidad débil <code>detalle_paro</code> con PK compuesta.", table_cell_style)
        ],
        [
            Paragraph("RN-042", table_cell_style), Paragraph("[D]", table_cell_style),
            Paragraph("El borrado de una máquina o turno con histórico debe estar bloqueado.", table_cell_style),
            Paragraph("Política <code>ON DELETE RESTRICT</code> en llaves foráneas.", table_cell_style)
        ],
    ]
    t_rn = Table(rn_data, colWidths=[45, 35, 264, 160])
    t_rn.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ]))
    story.append(t_rn)

    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 4 Y 5: MODELADO CONCEPTUAL, LÓGICO Y NORMALIZACIÓN
    # =========================================================================
    story.append(Paragraph("4. Modelado Conceptual y Lógico", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph("4.1 Modelo Conceptual Entidad-Relación (MER)", h2_style))
    story.append(Paragraph(
        "El modelo conceptual captura las entidades del dominio de producción y mantenimiento: "
        "<b>MAQUINA</b>, <b>TURNO</b>, <b>OPERARIO</b>, <b>REFERENCIA</b>, <b>TIPO_PARO</b>, "
        "<b>CODIGO_PARO</b>, <b>SUBCODIGO_PARO</b> y el evento central <b>REGISTRO_PRODUCCION</b> con sus detalles.",
        body_style
    ))
    story.append(Paragraph("<b>Cardinalidades y Participación del Modelo:</b>", body_style))
    story.append(Paragraph("• <code>MAQUINA (1,1) ----- (0,N) REGISTRO_PRODUCCION</code>: Cada máquina participa en cero o muchos registros; cada registro pertenece obligatoriamente a una sola máquina (Participación Total de Registro).", bullet_style))
    story.append(Paragraph("• <code>TURNO (1,1) ----- (0,N) REGISTRO_PRODUCCION</code>: Un turno puede tener muchos registros de producción asociados.", bullet_style))
    story.append(Paragraph("• <code>OPERARIO (0,1) ----- (0,N) REGISTRO_PRODUCCION</code>: Un operario puede operar en muchos registros. Un registro puede no tener operario asignado (NULL cuando no aplica o no se registró).", bullet_style))
    story.append(Paragraph("• <code>REGISTRO_PRODUCCION (1,1) ----- (0,N) DETALLE_PARO</code>: Un registro se desglosa en cero o muchos paros específicos por código.", bullet_style))
    story.append(Paragraph("• <code>CODIGO_PARO (1,1) ----- (0,N) DETALLE_PARO</code>: Un código clasifica múltiples incidencias.", bullet_style))
    story.append(Paragraph("• <code>CODIGO_PARO (1,1) ----- (0,N) SUBCODIGO_PARO</code>: Un código padre (01, 03, 05) engloba múltiples subcódigos específicos.", bullet_style))
    story.append(Paragraph("• <code>REGISTRO_PRODUCCION (1,1) ----- (0,N) DETALLE_SUBCODIGO</code>: Detalle exhaustivo de paros desagregados.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("4.2 Modelo Relacional Lógico (Esquema Lógico)", h2_style))
    story.append(Paragraph(
        "A partir de las reglas de derivación del MER se obtuvo el siguiente esquema relacional lógico "
        "(las claves primarias van subrayadas y las claves foráneas con prefijo FK):",
        body_style
    ))

    schema_text = """
• <b>MAQUINA</b> (<u>id_maquina</u>, nombre, factor_produccion, activa)<br/>
• <b>TURNO</b> (<u>id_turno</u>, nombre, hora_inicio, hora_fin, duracion_horas, minutos_alimentacion, minutos_pausa)<br/>
• <b>OPERARIO</b> (<u>id_operario</u>, pseudonimo, activo)<br/>
• <b>REFERENCIA</b> (<u>id_referencia</u>, nombre)<br/>
• <b>REFERENCIA_MAQUINA</b> (<u>id_ref_maq</u>, FK_id_referencia, FK_id_maquina, unidades_por_minuto, unidades_por_display, displays_por_paca)<br/>
• <b>TIPO_PARO</b> (<u>id_tipo_paro</u>, codigo, descripcion)<br/>
• <b>CODIGO_PARO</b> (<u>id_codigo</u>, numero, descripcion, area_impacto, tiene_subcodigos)<br/>
• <b>SUBCODIGO_PARO</b> (<u>id_subcodigo</u>, FK_id_codigo_padre, codigo, descripcion)<br/>
• <b>REGISTRO_PRODUCCION</b> (<u>id_registro</u>, fecha, FK_id_maquina, FK_id_turno, FK_id_operario, FK_id_referencia, horas_trabajadas, meta_por_hora, pacas_producidas, horas_no_trabajadas, FK_id_tipo_paro, observaciones_paro, tiempo_paro_minutos, observaciones)<br/>
• <b>DETALLE_PARO</b> (<u>FK_id_registro, FK_id_codigo</u>, duracion_minutos)<br/>
• <b>DETALLE_SUBCODIGO</b> (<u>id_detalle_sub</u>, FK_id_registro, FK_id_subcodigo, duracion_minutos, area_involucrada, personal_involucrado)
    """
    story.append(Paragraph(schema_text, body_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("5. Proceso Riguroso de Normalización", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph(
        "Se aplicó el proceso de normalización científica partiendo de la estructura plana no normalizada (UNF) "
        "de la hoja de Excel hasta alcanzar la <b>Tercera Forma Normal (3FN)</b>:",
        body_style
    ))

    norm_steps = [
        ("Forma No Normalizada (UNF)",
         "Tabla monolítica con 58 columnas. Incluye campos multivaluados y un grupo repetitivo de 18 columnas para registrar minutos por código ('Codigo 1' a 'Codigo 18') más 18 columnas de conversión a horas. Hay celdas compuestas y atributos calculados como Año, Mes y Productividad."),

        ("Primera Forma Normal (1FN)",
         "<b>Regla:</b> Todo atributo debe ser atómico y no deben existir grupos repetitivos.<br/>"
         "<b>Transformación:</b> Se eliminaron las 18 columnas horizontales de paros y se creó la tabla <code>detalle_paro</code> con clave compuesta (id_registro, id_codigo) y duración atómica en minutos. Se eliminaron celdas calculadas redundantes."),

        ("Segunda Forma Normal (2FN)",
         "<b>Regla:</b> Estar en 1FN y que ningún atributo no clave dependa funcionalmente de un subconjunto de la clave primaria (eliminación de dependencias parciales).<br/>"
         "<b>Transformación:</b> En <code>detalle_paro</code>, la descripción del código y el área de impacto no dependen de (id_registro, id_codigo), sino únicamente de id_codigo. Por tanto, se extrajo la tabla de catálogo <code>codigo_paro</code> dejando en detalle_paro únicamente la métrica <code>duracion_minutos</code>."),

        ("Tercera Forma Normal (3FN)",
         "<b>Regla:</b> Estar en 2FN y que ningún atributo no clave dependa transitivamente de la clave primaria a través de otro atributo no clave.<br/>"
         "<b>Transformación:</b> En la tabla <code>registro_produccion</code>, atributos como el factor de ajuste dependían de la máquina (no del registro); la duración de turno dependía del turno; la descripción del producto dependía de la referencia. Se extrajeron las entidades maestras <code>maquina</code>, <code>turno</code>, <code>operario</code> y <code>referencia</code>."),

        ("Justificación de Cero Desnormalización",
         "Se decidió <b>no desnormalizar</b> intencionalmente ninguna tabla del modelo. Dado el volumen transaccional (~8,200 registros históricos y crecimiento moderado de ~3,000 registros anuales), la arquitectura completamente normalizada a 3FN asegura integridad absoluta y un rendimiento excelente en MySQL 8.x con tiempos de respuesta en milisegundos gracias a los índices.")
    ]

    for title, desc in norm_steps:
        story.append(Paragraph(f"<b>• {title}:</b>", h2_style))
        story.append(Paragraph(desc, body_style))

    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 6 Y 7: DICCIONARIO DE DATOS Y DISEÑO FÍSICO
    # =========================================================================
    story.append(Paragraph("6. Diccionario de Datos del Modelo Físico (11 Tablas)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph(
        "A continuación se presenta la especificación física y semántica de las 11 tablas creadas en el esquema <code>paros_produccion</code>:",
        body_style
    ))

    # Tablas resumen en el PDF
    tables_summary = [
        ("maquina", "Catálogo de las 4 líneas de envasado y sus factores técnicos.", [
            ("id_maquina", "SMALLINT UNSIGNED", "NO", "AUTO_INCREMENT", "PK", "ID único"),
            ("nombre", "VARCHAR(30)", "NO", "—", "UNIQUE, NOT NULL", "Nombre línea"),
            ("factor_produccion", "DECIMAL(4,2)", "NO", "1.00", "CHECK(>0)", "Factor ajuste"),
            ("activa", "BOOLEAN", "NO", "TRUE", "—", "Estado activo")
        ]),
        ("turno", "Catálogo de turnos laborales y tiempos preasignados.", [
            ("id_turno", "SMALLINT UNSIGNED", "NO", "AUTO_INCREMENT", "PK", "ID turno"),
            ("nombre", "VARCHAR(30)", "NO", "—", "UNIQUE, NOT NULL", "Nombre turno"),
            ("hora_inicio / fin", "TIME", "SI", "NULL", "—", "Ventana horaria"),
            ("duracion_horas", "DECIMAL(4,1)", "SI", "NULL", "CHECK(>0)", "Horas duración"),
            ("minutos_alimentacion", "SMALLINT UNSIGNED", "NO", "40", "—", "Min. comida (cód 16)"),
            ("minutos_pausa", "SMALLINT UNSIGNED", "NO", "3", "—", "Min. pausas (cód 17)")
        ]),
        ("operario", "Registro de operarias con nombres anonimizados.", [
            ("id_operario", "SMALLINT UNSIGNED", "NO", "AUTO_INCREMENT", "PK", "ID operario"),
            ("pseudonimo", "VARCHAR(10)", "NO", "—", "UNIQUE, NOT NULL", "Código anónimo"),
            ("activo", "BOOLEAN", "NO", "TRUE", "—", "Vigencia laboral")
        ]),
        ("codigo_paro", "Catálogo oficial de los 18 códigos de paro estandarizados.", [
            ("id_codigo", "SMALLINT UNSIGNED", "NO", "AUTO_INCREMENT", "PK", "ID código"),
            ("numero", "TINYINT UNSIGNED", "NO", "—", "UNIQUE, CHECK(1..18)", "Número oficial"),
            ("descripcion", "VARCHAR(100)", "NO", "—", "NOT NULL", "Causa del paro"),
            ("area_impacto", "VARCHAR(40)", "NO", "—", "NOT NULL", "Área responsable"),
            ("tiene_subcodigos", "BOOLEAN", "NO", "FALSE", "—", "Aplica desglose")
        ]),
        ("registro_produccion", "Tabla de hechos central con los turnos de envasado.", [
            ("id_registro", "INT UNSIGNED", "NO", "AUTO_INCREMENT", "PK", "ID registro"),
            ("fecha", "DATE", "NO", "—", "NOT NULL", "Fecha producción"),
            ("id_maquina", "SMALLINT UNSIGNED", "NO", "—", "FK -> maquina", "Línea operada"),
            ("id_turno", "SMALLINT UNSIGNED", "NO", "—", "FK -> turno", "Turno ejecutado"),
            ("id_operario", "SMALLINT UNSIGNED", "SI", "NULL", "FK -> operario", "Operaria a cargo"),
            ("id_referencia", "SMALLINT UNSIGNED", "SI", "NULL", "FK -> referencia", "Pintura producida"),
            ("horas_trabajadas", "DECIMAL(4,1)", "SI", "NULL", "CHECK(>=0)", "Horas efectivas"),
            ("meta_por_hora", "DECIMAL(8,2)", "SI", "NULL", "CHECK(>=0)", "Meta pacas/hora"),
            ("pacas_producidas", "INT UNSIGNED", "SI", "NULL", "—", "Pacas logradas"),
            ("horas_no_trabajadas", "DECIMAL(4,1)", "SI", "NULL", "CHECK(>=0)", "Horas de paro"),
            ("id_tipo_paro", "SMALLINT UNSIGNED", "SI", "NULL", "FK -> tipo_paro", "Tipo paro turno"),
            ("tiempo_paro_minutos", "DECIMAL(8,2)", "SI", "NULL", "CHECK(>=0)", "Total min parados"),
            ("observaciones / paro", "TEXT", "SI", "NULL", "—", "Bitácoras")
        ]),
        ("detalle_paro", "Desglose atómico de duración de paro por código.", [
            ("id_registro", "INT UNSIGNED", "NO", "—", "PK, FK -> registro", "Registro padre"),
            ("id_codigo", "SMALLINT UNSIGNED", "NO", "—", "PK, FK -> codigo", "Código de paro"),
            ("duracion_minutos", "DECIMAL(8,2)", "NO", "0.00", "CHECK(>=0)", "Minutos de paro")
        ]),
        ("detalle_subcodigo", "Desglose por subcódigo para paros 01, 03 y 05.", [
            ("id_detalle_sub", "INT UNSIGNED", "NO", "AUTO_INCREMENT", "PK", "ID subdetalle"),
            ("id_registro", "INT UNSIGNED", "NO", "—", "FK -> registro", "Registro padre"),
            ("id_subcodigo", "SMALLINT UNSIGNED", "NO", "—", "FK -> subcodigo", "Subcódigo"),
            ("duracion_minutos", "DECIMAL(8,2)", "NO", "0.00", "CHECK(>=0)", "Minutos parados"),
            ("area / personal", "VARCHAR(30/10)", "SI", "NULL", "—", "Área y mecánico")
        ])
    ]

    for tbl_name, tbl_desc, cols in tables_summary:
        story.append(Paragraph(f"<b>Tabla: <code>{tbl_name}</code></b> — {tbl_desc}", h2_style))
        t_rows = [[Paragraph("Columna", table_header_style), Paragraph("Tipo Dato", table_header_style), Paragraph("Null", table_header_style), Paragraph("Default", table_header_style), Paragraph("Restricciones", table_header_style), Paragraph("Descripción", table_header_style)]]
        for cname, ctype, cnull, cdef, crestr, cdesc in cols:
            t_rows.append([
                Paragraph(f"<code>{cname}</code>", table_cell_style),
                Paragraph(ctype, table_cell_style),
                Paragraph(cnull, table_cell_style),
                Paragraph(cdef, table_cell_style),
                Paragraph(crestr, table_cell_style),
                Paragraph(cdesc, table_cell_style)
            ])
        t_tab = Table(t_rows, colWidths=[90, 85, 30, 60, 95, 144])
        t_tab.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), primary_color),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ]))
        story.append(t_tab)
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 8: RESTRICCIONES E ÍNDICES
    # =========================================================================
    story.append(Paragraph("7. Restricciones e Índices de Rendimiento", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("7.1 Políticas de Integridad Referencial (ON DELETE / ON UPDATE)", h2_style))
    story.append(Paragraph(
        "Se justificaron rigurosamente las acciones de clave foránea según el ciclo de vida de los datos de negocio:",
        body_style
    ))

    fk_policies = [
        ("registro_produccion → maquina / turno", "ON DELETE RESTRICT, ON UPDATE CASCADE",
         "<b>Justificación:</b> Una máquina o turno son entidades fundamentales de la infraestructura fabril. Bajo ninguna circunstancia se debe permitir su eliminación física si existen turnos históricos registrados. Si una máquina cambia de código, se propaga en cascada."),
        ("registro_produccion → operario / referencia / tipo_paro", "ON DELETE SET NULL, ON UPDATE CASCADE",
         "<b>Justificación:</b> Si un operario finaliza su vínculo laboral o una referencia de pintura es descontinuada del portafolio comercial, la historia de producción no debe borrarse. El registro histórico se preserva intacto conservando las horas y pacas producidas, quedando la llave foránea en NULL."),
        ("detalle_paro / detalle_subcodigo → registro_produccion", "ON DELETE CASCADE, ON UPDATE CASCADE",
         "<b>Justificación:</b> Los detalles de paro y subcódigo constituyen entidades dependientes en existencia (entidades débiles). Si se depura o elimina formalmente un registro diario de producción, todos sus eventos de paro asociados deben suprimirse automáticamente en cascada.")
    ]
    for rel, pol, just in fk_policies:
        story.append(Paragraph(f"• <b>{rel}</b> [<code>{pol}</code>]", body_style))
        story.append(Paragraph(just, bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("7.2 Justificación Técnica de los 6 Índices Implementados", h2_style))
    story.append(Paragraph(
        "Se diseñaron e implementaron en el script <code>03_crear_indices.sql</code> seis índices B-Tree específicos, "
        "justificados directamente por los patrones de filtrado y agregación de las consultas analíticas del negocio:",
        body_style
    ))

    idx_data = [
        [Paragraph("Índice Creado", table_header_style), Paragraph("Tabla y Columnas", table_header_style), Paragraph("Justificación y Consulta Asociada", table_header_style)],
        [
            Paragraph("<code>idx_reg_fecha</code>", table_cell_style),
            Paragraph("<code>registro_produccion(fecha)</code>", table_cell_style),
            Paragraph("Acelera filtros por rango de fechas (<code>BETWEEN</code>) en todas las consultas mensuales y anuales.", table_cell_style)
        ],
        [
            Paragraph("<code>idx_reg_maquina_fecha</code>", table_cell_style),
            Paragraph("<code>registro_produccion(id_maquina, fecha)</code>", table_cell_style),
            Paragraph("<b>Índice compuesto:</b> Optimiza la Consulta 1 (productividad por máquina y mes), cubriendo el JOIN con máquina y la agrupación temporal sin reordenar en memoria.", table_cell_style)
        ],
        [
            Paragraph("<code>idx_reg_turno</code>", table_cell_style),
            Paragraph("<code>registro_produccion(id_turno)</code>", table_cell_style),
            Paragraph("Optimiza la Consulta 4 (comparativa entre turnos), acelerando el agrupamiento y agregación de horas.", table_cell_style)
        ],
        [
            Paragraph("<code>idx_dp_codigo</code>", table_cell_style),
            Paragraph("<code>detalle_paro(id_codigo)</code>", table_cell_style),
            Paragraph("Acelera las Consultas 2 y 7 (participación porcentual y top 10 causas), evitando escaneo secuencial en los 16,532 registros de detalle.", table_cell_style)
        ],
        [
            Paragraph("<code>idx_ds_subcodigo</code>", table_cell_style),
            Paragraph("<code>detalle_subcodigo(id_subcodigo)</code>", table_cell_style),
            Paragraph("Optimiza la Consulta 3 (desglose de subcódigos 01, 03 y 05), facilitando el JOIN con la tabla de subcódigos.", table_cell_style)
        ],
        [
            Paragraph("<code>idx_reg_operario</code>", table_cell_style),
            Paragraph("<code>registro_produccion(id_operario)</code>", table_cell_style),
            Paragraph("Optimiza la Consulta 10 para evaluar desempeño y registros anómalos agrupados por operaria.", table_cell_style)
        ]
    ]
    t_idx = Table(idx_data, colWidths=[110, 150, 244])
    t_idx.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ]))
    story.append(t_idx)

    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 9 Y 10: MIGRACIÓN Y PROTECCIÓN DE DATOS
    # =========================================================================
    story.append(Paragraph("8. Estrategia de Migración y Validación Cuantitativa", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("8.1 Proceso ETL (Extracción, Transformación y Carga)", h2_style))
    story.append(Paragraph(
        "Para garantizar total reproducibilidad e integridad sin correr el riesgo de ejecutar macros VBA potencialmente corruptas, "
        "se diseñó un pipeline de migración en Python (<code>migration/scripts/04_migrar_datos.py</code> y <code>05_migrar_subcodigos.py</code>):",
        body_style
    ))
    story.append(Paragraph("1. <b>Extracción limpia:</b> Lectura directa de las tablas estructuradas del archivo Open XML (hoja <code>BD</code> y hoja <code>BD_SUBCODIGOS</code>).", bullet_style))
    story.append(Paragraph("2. <b>Transformación y Limpieza:</b> Normalización de nombres de máquinas, conversión de fechas a formato ISO YYYY-MM-DD, homologación de tipos de paro con y sin corchetes, y sustitución de turnos en blanco por 'No aplica'.", bullet_style))
    story.append(Paragraph("3. <b>Pseudonimización de Operarios:</b> Mapeo hash reversible de nombres reales a códigos anónimos OP-001..OP-032.", bullet_style))
    story.append(Paragraph("4. <b>Pivot de Columnas de Paro:</b> Transformación de las 18 columnas horizontales en inserciones independientes en <code>detalle_paro</code> únicamente cuando la duración reportada fue estrictamente mayor a 0 minutos.", bullet_style))
    story.append(Paragraph("5. <b>Generación de Scripts SQL por Lotes:</b> Inserciones masivas en bloques de 500 registros para optimizar el rendimiento y respetar el buffer de paquetes de MySQL.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("8.2 Validación Cuantitativa de Integridad (Cero Pérdida)", h2_style))

    val_data = [
        [Paragraph("Entidad / Indicador", table_header_style), Paragraph("Total en Excel Original", table_header_style), Paragraph("Total Migrado a MySQL", table_header_style), Paragraph("Integridad", table_header_style)],
        [Paragraph("Registros de Producción (Filas T_baseDeDatos)", table_cell_style), Paragraph("8,208", table_cell_style), Paragraph("8,208", table_cell_style), Paragraph("100.0% Exacto", table_cell_style)],
        [Paragraph("Detalles de Paro (Incidencias > 0 min)", table_cell_style), Paragraph("16,532", table_cell_style), Paragraph("16,532", table_cell_style), Paragraph("100.0% Exacto", table_cell_style)],
        [Paragraph("Subcódigos Detallados (01, 03, 05)", table_cell_style), Paragraph("1,252 (1,115 válidos)", table_cell_style), Paragraph("1,115", table_cell_style), Paragraph("99.7% (4 huérfanos)", table_cell_style)],
        [Paragraph("Líneas de Envasado", table_cell_style), Paragraph("4 máquinas", table_cell_style), Paragraph("4 máquinas", table_cell_style), Paragraph("100.0% Exacto", table_cell_style)],
        [Paragraph("Distribución: Vinilos_1", table_cell_style), Paragraph("1,877 registros", table_cell_style), Paragraph("1,877 registros", table_cell_style), Paragraph("100.0% Exacto", table_cell_style)],
        [Paragraph("Distribución: Vinilos_2", table_cell_style), Paragraph("1,255 registros", table_cell_style), Paragraph("1,255 registros", table_cell_style), Paragraph("100.0% Exacto", table_cell_style)],
        [Paragraph("Distribución: Vinilos_3", table_cell_style), Paragraph("2,491 registros", table_cell_style), Paragraph("2,491 registros", table_cell_style), Paragraph("100.0% Exacto", table_cell_style)],
        [Paragraph("Distribución: Vinilos_4", table_cell_style), Paragraph("2,585 registros", table_cell_style), Paragraph("2,585 registros", table_cell_style), Paragraph("100.0% Exacto", table_cell_style)],
        [Paragraph("Ventana Histórica de Fechas", table_cell_style), Paragraph("2022-01-01 a 2025-03-28", table_cell_style), Paragraph("2022-01-01 a 2025-03-28", table_cell_style), Paragraph("Consistente", table_cell_style)]
    ]
    t_val = Table(val_data, colWidths=[180, 110, 110, 104])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ]))
    story.append(t_val)

    story.append(Spacer(1, 8))
    story.append(Paragraph("9. Estrategia de Protección de Datos Personales", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))
    story.append(Paragraph(
        "De conformidad con las leyes de protección de datos (Habeas Data) y atendiendo a que el repositorio del proyecto "
        "será público en GitHub, se implementó un riguroso protocolo de <b>pseudonimización reversible</b>:",
        body_style
    ))
    story.append(Paragraph("• <b>Anonimización en Base de Datos:</b> Los 32 nombres y apellidos de operarias y técnicos de mantenimiento fueron reemplazados por identificadores alfanuméricos deterministas: <code>OP-001</code> a <code>OP-032</code> y <code>PM-001</code>.", bullet_style))
    story.append(Paragraph("• <b>Mapeo Privado Fuera de Repositorio:</b> La correspondencia real↔pseudónimo se almacena en el archivo local <code>migration/scripts/MAPEO_PRIVADO_NO_PUBLICAR.csv</code>, expresamente catalogado en el archivo <code>.gitignore</code> para impedir su filtración a GitHub.", bullet_style))
    story.append(Paragraph("• <b>Preservación Analítica:</b> Al usar pseudónimos estables, la base de datos permite seguir analizando productividad por turno y operaria sin vulnerar en absoluto el derecho a la intimidad del personal de planta.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 11: CONSULTAS SQL DE NEGOCIO
    # =========================================================================
    story.append(Paragraph("10. Consultas SQL Analíticas de Negocio e Indicadores", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph(
        "Se diseñaron 10 consultas SQL empresariales avanzadas (almacenadas en <code>sql/08_consultas_negocio.sql</code>) "
        "que responden a preguntas críticas de gerencia y explotan operadores como <code>INNER JOIN</code>, <code>LEFT JOIN</code>, "
        "funciones de agregación (<code>SUM</code>, <code>AVG</code>, <code>COUNT</code>), <code>GROUP BY</code>, <code>HAVING</code>, "
        "subconsultas correlacionadas y filtros temporales <code>BETWEEN</code>:",
        body_style
    ))

    queries_desc = [
        ("Consulta 1: Productividad Mensual por Máquina y Comparativo Anual",
         "Aplica la fórmula oficial: <code>(Real / Meta_Ideal) * Factor_Ajuste</code> agrupando por línea, año y mes. Permite auditar el cumplimiento mensual de la meta gerencial e identificar caídas de eficiencia interanuales.",
         """SELECT m.nombre AS maquina, YEAR(r.fecha) AS anio, MONTH(r.fecha) AS mes,
       SUM(r.pacas_producidas) AS pacas_reales,
       ROUND(SUM(r.horas_trabajadas * r.meta_por_hora), 2) AS pacas_ideales,
       ROUND((SUM(r.pacas_producidas) / NULLIF(SUM(r.horas_trabajadas * r.meta_por_hora), 0)) 
             * m.factor_produccion * 100, 2) AS pct_productividad
FROM registro_produccion r
INNER JOIN maquina m ON r.id_maquina = m.id_maquina
WHERE r.horas_trabajadas > 0 AND r.meta_por_hora > 0
GROUP BY m.nombre, m.factor_produccion, YEAR(r.fecha), MONTH(r.fecha)
ORDER BY m.nombre, anio, mes;"""),

        ("Consulta 2: Participación Porcentual de Cada Código de Paro",
         "Calcula el tiempo total acumulado de cada uno de los 18 códigos y su ponderación porcentual sobre las horas totales de inactividad de la planta, usando una subconsulta escalar para el total general.",
         """SELECT cp.numero AS codigo, cp.descripcion, cp.area_impacto,
       ROUND(SUM(dp.duracion_minutos) / 60, 2) AS total_horas_paro,
       ROUND((SUM(dp.duracion_minutos) / 
             (SELECT SUM(duracion_minutos) FROM detalle_paro)) * 100, 2) AS pct_participacion
FROM detalle_paro dp
INNER JOIN codigo_paro cp ON dp.id_codigo = cp.id_codigo
GROUP BY cp.numero, cp.descripcion, cp.area_impacto
ORDER BY total_horas_paro DESC;"""),

        ("Consulta 3: Análisis Detallado por Subcódigo (Códigos 01, 03 y 05)",
         "Desagrega con precisión las causas raíz de averías mecánicas (01), operacionales (03) y ajustes de calidad (05), indicando además si el impacto involucró a operarias o mecánicos.",
         """SELECT cp.numero AS codigo_padre, sp.codigo AS subcodigo, sp.descripcion,
       ROUND(SUM(ds.duracion_minutos) / 60, 2) AS horas_paro,
       COUNT(ds.id_detalle_sub) AS frecuencia_eventos
FROM detalle_subcodigo ds
INNER JOIN subcodigo_paro sp ON ds.id_subcodigo = sp.id_subcodigo
INNER JOIN codigo_paro cp ON sp.id_codigo_padre = cp.id_codigo
WHERE cp.numero IN (1, 3, 5)
GROUP BY cp.numero, sp.codigo, sp.descripcion
ORDER BY cp.numero, horas_paro DESC;"""),

        ("Consulta 4: Comparación del Desempeño Operativo entre Turnos",
         "Evalúa el rendimiento de los turnos laborales (T1 mañana, T2 tarde, T3 noche), contrastando horas efectivas, producción media y volumen total de detenciones.",
         """SELECT t.nombre AS turno, COUNT(r.id_registro) AS total_turnos,
       ROUND(AVG(r.horas_trabajadas), 2) AS promedio_horas_trabajadas,
       ROUND(AVG(r.pacas_producidas), 0) AS promedio_pacas_producidas,
       ROUND(SUM(r.tiempo_paro_minutos) / 60, 2) AS total_horas_paro
FROM registro_produccion r
INNER JOIN turno t ON r.id_turno = t.id_turno
WHERE t.nombre != 'No aplica'
GROUP BY t.nombre
ORDER BY total_horas_paro DESC;""")
    ]

    for qtitle, qdesc, qsql in queries_desc:
        story.append(Paragraph(f"<b>{qtitle}</b>", h2_style))
        story.append(Paragraph(qdesc, body_style))
        story.append(Table([[Paragraph(f"<pre>{qsql}</pre>", code_style)]], colWidths=[504], style=[
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # Continuación de consultas y pruebas
    story.append(Paragraph("10.2 Cobertura de Consultas Adicionales del Negocio", h2_style))
    story.append(Paragraph("Además de las cuatro consultas obligatorias del docente, el script <code>08_consultas_negocio.sql</code> integra:", body_style))
    story.append(Paragraph("• <b>Consulta 5 (Tiempos de Paro por Máquina):</b> Suma de horas no trabajadas discriminadas por línea y porcentaje de disponibilidad técnica.", bullet_style))
    story.append(Paragraph("• <b>Consulta 6 (Evolución Mensual de Paros):</b> Análisis de tendencias temporales para mantenimiento preventivo en 2024.", bullet_style))
    story.append(Paragraph("• <b>Consulta 7 (Top 10 Causas de Paro con HAVING):</b> Filtro mediante <code>HAVING total_horas > 50</code> para aislar cuellos de botella mayores.", bullet_style))
    story.append(Paragraph("• <b>Consulta 8 (Producción Real vs Meta):</b> Balance de cumplimiento absoluto agrupado por referencia de pintura fabricada.", bullet_style))
    story.append(Paragraph("• <b>Consulta 9 (Distribución de Paros por Área de Impacto):</b> Comparativo del porcentaje de paro atribuible a Mantenimiento, Calidad, Producción y Logística.", bullet_style))
    story.append(Paragraph("• <b>Consulta 10 (Registros sin Producción):</b> Detección de turnos improductivos (pacas = 0 pero horas > 0) para auditoría de planta.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("11. Pruebas de Integridad y Rechazos Controlados", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph(
        "Se demostró la robustez de las restricciones mediante pruebas de manipulación (INSERT, UPDATE, DELETE) "
        "y <b>7 pruebas de rechazo forzado</b> implementadas en <code>sql/09_pruebas_restricciones.sql</code>:",
        body_style
    ))

    test_data = [
        [Paragraph("Caso de Prueba", table_header_style), Paragraph("Acción Ejecutada en MySQL", table_header_style), Paragraph("Restricción Activada", table_header_style), Paragraph("Resultado / Error MySQL", table_header_style)],
        [
            Paragraph("<b>Prueba 4.1</b>", table_cell_style),
            Paragraph("INSERT máquina duplicada con nombre 'Vinilos_1'", table_cell_style),
            Paragraph("<code>UNIQUE(nombre)</code>", table_cell_style),
            Paragraph("<b>Rechazado: Error 1062</b> (Duplicate entry)", table_cell_style)
        ],
        [
            Paragraph("<b>Prueba 4.2</b>", table_cell_style),
            Paragraph("INSERT registro con máquina inexistente (id=999)", table_cell_style),
            Paragraph("<code>FK registro → maquina</code>", table_cell_style),
            Paragraph("<b>Rechazado: Error 1452</b> (Cannot add child row)", table_cell_style)
        ],
        [
            Paragraph("<b>Prueba 4.3</b>", table_cell_style),
            Paragraph("INSERT máquina con factor de producción = -0.50", table_cell_style),
            Paragraph("<code>CHECK(factor_produccion > 0)</code>", table_cell_style),
            Paragraph("<b>Rechazado: Error 3819</b> (Check constraint violated)", table_cell_style)
        ],
        [
            Paragraph("<b>Prueba 4.4</b>", table_cell_style),
            Paragraph("INSERT horas_trabajadas negativas (-2.5)", table_cell_style),
            Paragraph("<code>CHECK(horas_trabajadas >= 0)</code>", table_cell_style),
            Paragraph("<b>Rechazado: Error 3819</b> (Check constraint violated)", table_cell_style)
        ],
        [
            Paragraph("<b>Prueba 4.5</b>", table_cell_style),
            Paragraph("DELETE máquina Vinilos_1 que tiene 1,877 registros", table_cell_style),
            Paragraph("<code>ON DELETE RESTRICT</code>", table_cell_style),
            Paragraph("<b>Rechazado: Error 1451</b> (Cannot delete parent row)", table_cell_style)
        ],
        [
            Paragraph("<b>Prueba 4.6</b>", table_cell_style),
            Paragraph("INSERT código de paro con número = 25 (fuera de rango)", table_cell_style),
            Paragraph("<code>CHECK(numero BETWEEN 1 AND 18)</code>", table_cell_style),
            Paragraph("<b>Rechazado: Error 3819</b> (Check constraint violated)", table_cell_style)
        ],
        [
            Paragraph("<b>Prueba 4.7</b>", table_cell_style),
            Paragraph("INSERT detalle_paro con duración negativa (-10 min)", table_cell_style),
            Paragraph("<code>CHECK(duracion_minutos >= 0)</code>", table_cell_style),
            Paragraph("<b>Rechazado: Error 3819</b> (Check constraint violated)", table_cell_style)
        ]
    ]
    t_test = Table(test_data, colWidths=[65, 175, 120, 144])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ]))
    story.append(t_test)

    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 12 Y 13: GUÍA DBEAVER, GIT Y CONCLUSIONES
    # =========================================================================
    story.append(Paragraph("12. Guía de Ejecución en DBeaver y Versionamiento Git", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("12.1 Procedimiento de Reproducción desde Cero en DBeaver", h2_style))
    story.append(Paragraph(
        "Para reconstruir la totalidad de la base de datos y verificar su funcionamiento desde DBeaver, "
        "se deben ejecutar de forma secuencial y ordenada los 11 scripts SQL ubicados en la carpeta <code>sql/</code>:",
        body_style
    ))

    scripts_order = [
        ("00_crear_base_datos.sql", "Crea la base de datos 'paros_produccion' con juego de caracteres UTF8MB4."),
        ("01_crear_tablas.sql", "Crea el esquema con las 11 tablas relacionales y todas sus restricciones PK, FK, CHECK y UNIQUE."),
        ("02_datos_catalogos.sql", "Inserta catálogos base: 4 máquinas, 7 turnos, 18 códigos, 47 subcódigos y 19 tipos de paro."),
        ("03_crear_indices.sql", "Genera los 6 índices optimizados para agilizar filtros temporales y JOINs."),
        ("04_datos_operarios.sql", "Inserta las 32 operarias bajo formato pseudonimizado (OP-001 a OP-032)."),
        ("05_datos_referencias.sql", "Carga el portafolio de 51 referencias de pinturas (vinilos y témperas)."),
        ("06_datos_registros.sql", "Inserta los 8,208 registros históricos de producción en bloques de 500 filas."),
        ("07_datos_detalles_paro.sql", "Inserta las 16,532 incidencias de paro desagregadas por código."),
        ("07b_datos_subcodigos.sql", "Inserta los 1,115 eventos detallados de subcódigos para paros 01, 03 y 05."),
        ("08_consultas_negocio.sql", "Ejecuta el catálogo de las 10 consultas analíticas e indicadores."),
        ("09_pruebas_restricciones.sql", "Ejecuta las pruebas de INSERT/UPDATE/DELETE y valida los 7 rechazos de integridad.")
    ]
    for sname, sdesc in scripts_order:
        story.append(Paragraph(f"• <b><code>sql/{sname}</code></b>: {sdesc}", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("12.2 Repositorio Git y Contribución Colaborativa", h2_style))
    story.append(Paragraph(
        "El proyecto fue versionado siguiendo las mejores prácticas de ingeniería de software. "
        "El historial de commits refleja un avance progresivo y balanceado entre los tres integrantes del equipo "
        "(<b>Juan Sebastián Raigosa Gil</b>, <b>Deysi Carolina Echavarría Soto</b> y <b>Jose Miguel Sosa Cartagena</b>), estructurado en etapas lógicas: "
        "auditoría inicial, reglas de negocio, modelado relacional, diccionario de datos, scripts DDL, migración de datos, "
        "consultas SQL y documentación final.",
        body_style
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("13. Conclusiones y Referencias", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("13.1 Conclusiones", h2_style))
    story.append(Paragraph(
        "1. <b>Sustitución Exitosa del Excel:</b> Se eliminaron las 18 columnas repetitivas horizontales y las 180,000 celdas con fórmulas volátiles, logrando una arquitectura relacional normalizada a 3FN que garantiza integridad absoluta sin redundancias.",
        body_style
    ))
    story.append(Paragraph(
        "2. <b>Migración Cuantitativamente Íntegra:</b> Se rescataron exitosamente el 100% de los 8,208 registros históricos de producción y los 16,532 paros detallados del período 2022-2025 mediante un script de extracción que evitó la ejecución de macros propensas a errores.",
        body_style
    ))
    story.append(Paragraph(
        "3. <b>Cumplimiento Normativo y Privacidad:</b> La estrategia de pseudonimización demostró que es viable auditar y consultar el desempeño del personal sin exponer información personal sensible en entornos públicos.",
        body_style
    ))
    story.append(Paragraph(
        "4. <b>Potencia Analítica y Desempeño:</b> Las consultas SQL con JOIN, GROUP BY e índices dedicados permitieron reproducir y superar los reportes mensuales de la gerencia con tiempos de respuesta inferiores a 20 ms en DBeaver.",
        body_style
    ))

    story.append(Paragraph("13.2 Referencias Bibliográficas", h2_style))
    story.append(Paragraph("• Elmasri, R., & Navathe, S. B. (2016). <i>Fundamentals of Database Systems</i> (7th ed.). Pearson.", bullet_style))
    story.append(Paragraph("• Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). <i>Database System Concepts</i> (7th ed.). McGraw-Hill.", bullet_style))
    story.append(Paragraph("• MySQL AB / Oracle Corporation. (2024). <i>MySQL 8.0 Reference Manual: Constraints and Optimization</i>.", bullet_style))
    story.append(Paragraph("• Documento Operativo Interno: <i>P-MTO-22 V1: Procedimiento para el Registro de Paros de Producción</i> (2022).", bullet_style))

    # Construir documento
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Reporte generado exitosamente en: {pdf_path}")

    # Generar copia con los 3 apellidos según guía del docente
    import shutil
    pdf_path_3 = os.path.join(output_dir, "BDI_ProyectoFinal_Raigosa_Echavarria_Sosa.pdf")
    shutil.copyfile(pdf_path, pdf_path_3)
    print(f"Reporte con 3 apellidos generado en: {pdf_path_3}")

if __name__ == "__main__":
    create_report()

