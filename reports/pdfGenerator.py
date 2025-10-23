import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

def _build_header(doc_title, fecha_hora):
    style = ParagraphStyle(name='default', fontSize=10, alignment=TA_LEFT)
    texto = f"Empresa StayAway Co<br/>{doc_title}<br/>Fecha: {fecha_hora}"
    return Paragraph(texto, style)

def generate_movements_pdf(rows, columns, doc_title="Reporte", fecha_hora="N/A", logo_path=None):
    """
    rows: list of lists (data rows)
    columns: header list
    devuelve BytesIO con el PDF (posición al inicio)
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)

    elements = []
    if logo_path:
        try:
            img = Image(logo_path, width=80, height=80)
            elements.append(img)
            elements.append(Spacer(1, 6))
        except Exception:
            pass

    elements.append(_build_header(doc_title, fecha_hora))
    elements.append(Spacer(1, 12))

    data = [columns] + list(rows)
    table = Table(data, hAlign='LEFT')
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#eeeeee")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ])
    table.setStyle(style)
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer