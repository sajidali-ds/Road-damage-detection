import os
from datetime import datetime

import pandas as pd
from fpdf import FPDF

from config import EXCEL_REPORTS_DIR, PDF_REPORTS_DIR

os.makedirs(EXCEL_REPORTS_DIR, exist_ok=True)
os.makedirs(PDF_REPORTS_DIR, exist_ok=True)


def generate_excel_report(predicted_class, confidence, lat, lon, address, created_at=None) -> str:
    """Creates a one-row Excel report and returns the saved file path."""
    created_at = created_at or datetime.now().isoformat()
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    path = os.path.join(EXCEL_REPORTS_DIR, filename)

    df = pd.DataFrame([{
        "Predicted Class": predicted_class,
        "Confidence (%)": round(confidence * 100, 2),
        "Latitude": lat,
        "Longitude": lon,
        "Address": address,
        "Reported At": created_at,
    }])
    df.to_excel(path, index=False)
    return path


def generate_pdf_report(predicted_class, confidence, lat, lon, address,
                         image_path: str | None = None, created_at=None) -> str:
    """Creates a simple one-page PDF report and returns the saved file path."""
    created_at = created_at or datetime.now().isoformat()
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = os.path.join(PDF_REPORTS_DIR, filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Road Damage Report", ln=True)

    pdf.set_font("Helvetica", "", 12)
    pdf.ln(4)
    pdf.cell(0, 8, f"Predicted class: {predicted_class}", ln=True)
    pdf.cell(0, 8, f"Confidence: {confidence * 100:.2f}%", ln=True)
    pdf.cell(0, 8, f"Location: {lat}, {lon}", ln=True)
    pdf.multi_cell(0, 8, f"Address: {address}")
    pdf.cell(0, 8, f"Reported at: {created_at}", ln=True)

    if image_path and os.path.exists(image_path):
        pdf.ln(4)
        pdf.image(image_path, w=150)

    pdf.output(path)
    return path
