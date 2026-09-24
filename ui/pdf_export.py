from __future__ import annotations

import os
import platform
from datetime import datetime
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


EXPORT_DIR = Path(__file__).resolve().parent.parent / "exports"
FONT_NAME = "ElaiaSans"


def _register_font() -> str:
    candidates = {
        "Windows": [Path(r"C:\Windows\Fonts\arial.ttf")],
        "Darwin": [
            Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
            Path("/Library/Fonts/Arial.ttf"),
        ],
    }.get(platform.system(), [])
    for font_path in candidates:
        if font_path.exists():
            pdfmetrics.registerFont(TTFont(FONT_NAME, str(font_path)))
            return FONT_NAME
    return "Helvetica"


def _display_value(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(_display_value(item) for item in value) or "Yok"
    if isinstance(value, dict):
        return "; ".join(f"{key}: {_display_value(item)}" for key, item in value.items())
    return str(value) if value not in (None, "") else "Yok"


def export_department_pdf(department: str, report: dict[str, Any]) -> Path:
    """Create a standalone PDF for one department's metrics and AI analysis."""
    EXPORT_DIR.mkdir(exist_ok=True)
    safe_name = "".join(character if character.isalnum() else "_" for character in department)
    path = EXPORT_DIR / f"{safe_name}_{datetime.now():%Y%m%d_%H%M%S}.pdf"
    font_name = _register_font()
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "ElaiaTitle",
        parent=styles["Title"],
        fontName=font_name,
        fontSize=22,
        leading=27,
        textColor=colors.HexColor("#173B37"),
        spaceAfter=6 * mm,
    )
    heading = ParagraphStyle(
        "ElaiaHeading",
        parent=styles["Heading2"],
        fontName=font_name,
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#B55A34"),
        spaceBefore=5 * mm,
        spaceAfter=3 * mm,
    )
    body = ParagraphStyle(
        "ElaiaBody",
        parent=styles["BodyText"],
        fontName=font_name,
        fontSize=9.5,
        leading=14,
        alignment=TA_LEFT,
    )
    document = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=f"Elaia Ceramics | {department}",
    )

    metrics = report.get("metrikler", report)
    rows = [
        [
            Paragraph(str(label).replace("_", " ").title(), body),
            Paragraph(_display_value(value), body),
        ]
        for label, value in metrics.items()
        if label != "yapay_zeka_analizi"
    ]
    table = Table(rows, colWidths=[57 * mm, 105 * mm], repeatRows=0)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E7EEE9")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B8CBC1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    analysis = report.get("yapay_zeka_analizi", "Yapay zeka analizi bulunamadi.")
    story = [
        Paragraph("Elaia Ceramics", body),
        Paragraph(department, title),
        Paragraph(f"Olusturma tarihi: {datetime.now():%d.%m.%Y %H:%M}", body),
        Spacer(1, 5 * mm),
        Paragraph("Operasyonel Metrikler", heading),
        KeepTogether(table),
        Paragraph("Llama 3.2 Analizi", heading),
        Paragraph(analysis.replace("\n", "<br/>"), body),
    ]
    document.build(story)
    return path
