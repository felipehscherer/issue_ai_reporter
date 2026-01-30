import os
from datetime import datetime
from typing import Dict

from fpdf import FPDF

from src.application.ports.out.pdf_renderer_port import PdfRendererPort


class FpdfRendererAdapter(PdfRendererPort):
    def __init__(self, config: Dict[str, str] | None = None) -> None:
        self._config = config or {}

    def render(self, text: str, metadata: Dict[str, str], output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.add_font("DejaVu", "", "C:/Windows/Fonts/arial.ttf", uni=True)
        pdf.set_font("DejaVu", "", 16)
        pdf.cell(0, 10, "Relatorio de Qualidade", ln=True, align="C")
        pdf.ln(5)

        pdf.set_font("DejaVu", "", 11)
        pdf.cell(0, 8, f"Card ID: {metadata.get('card_id')}", ln=True)
        pdf.cell(0, 8, f"Titulo: {metadata.get('title')}", ln=True)
        pdf.cell(0, 8, f"Tipo: {metadata.get('card_type')}", ln=True)
        pdf.cell(0, 8, f"Relatorio: {metadata.get('report_type')}", ln=True)
        pdf.cell(0, 8, f"Fonte: {metadata.get('source')}", ln=True)
        pdf.cell(0, 8, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
        pdf.ln(6)

        pdf.set_draw_color(0, 0, 0)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(8)

        pdf.set_font("DejaVu", "", 11)
        pdf.multi_cell(0, 6, text)

        filename = f"relatorio_{metadata.get('report_type')}_{metadata.get('card_id')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        path = os.path.join(output_dir, filename)
        pdf.output(path)
        return path
