#!/usr/bin/env python3
"""
Generate PDF from listen_lv.csv

Parses the CSV file and generates a PDF document
with a structured list of all teaching assignments.
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Error: reportlab is not installed. Install with: pip install reportlab")
    sys.exit(1)


def read_csv(filepath: Path) -> list[dict]:
    """Read CSV file and return list of entries."""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        return list(reader)


def create_pdf(entries: list[dict], output_path: Path) -> int:
    """Create a PDF document from the teaching entries."""
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=10,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#666666')
    )

    category_style = ParagraphStyle(
        'CategoryStyle',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=15,
        spaceAfter=8,
        textColor=colors.HexColor('#333333')
    )

    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=8,
        leading=10
    )

    small_style = ParagraphStyle(
        'SmallStyle',
        parent=styles['Normal'],
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#666666')
    )

    # Build content
    story = []

    # Title
    story.append(Paragraph("Lehrveranstaltungen", title_style))
    story.append(Paragraph("Jan Vanvinkenroye", subtitle_style))

    # Summary statistics
    categories = defaultdict(int)
    institutions = defaultdict(int)
    for entry in entries:
        cats = entry['Kategorien'].replace('"', '').split('; ')
        for cat in cats:
            if cat.strip():
                categories[cat.strip()] += 1
        institutions[entry['Hochschule']] += 1

    summary = f"Gesamt: {len(entries)} Lehrveranstaltungen an {len(institutions)} Hochschulen"
    story.append(Paragraph(summary, small_style))
    story.append(Spacer(1, 15))

    # Group by institution
    by_institution = defaultdict(list)
    for entry in entries:
        by_institution[entry['Hochschule']].append(entry)

    # Sort institutions by number of entries (descending)
    sorted_institutions = sorted(by_institution.items(), key=lambda x: -len(x[1]))

    # Create table for each institution
    for institution, inst_entries in sorted_institutions:
        # Institution header
        story.append(Paragraph(f"{institution} ({len(inst_entries)})", category_style))

        # Table data
        table_data = [['Lehrveranstaltung', 'Semester', 'Studiengang', 'Kategorien']]

        for entry in inst_entries:
            standort = entry.get('Standort', '')
            lv = entry['Lehrveranstaltung']
            if standort:
                lv = f"{lv}<br/><font size='6' color='#888888'>Standort: {standort}</font>"

            semester = entry['Semester'] or '–'
            studiengang = entry['Studiengang'].replace('"', '').replace('; ', '<br/>')
            kategorien = entry['Kategorien'].replace('"', '').replace('; ', '<br/>')

            table_data.append([
                Paragraph(lv, normal_style),
                Paragraph(semester, normal_style),
                Paragraph(studiengang, small_style),
                Paragraph(kategorien, small_style)
            ])

        # Create table
        col_widths = [6.5*cm, 2.2*cm, 4.5*cm, 4*cm]
        table = Table(table_data, colWidths=col_widths, repeatRows=1)

        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8e8e8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#333333')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),

            # Body
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),

            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),

            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))

        story.append(table)
        story.append(Spacer(1, 10))

    # Add temporal distribution of categories
    story.append(Spacer(1, 20))
    story.append(Paragraph("Themen-Schwerpunkte nach Zeit", category_style))

    # Extract years and map categories to years
    import re
    year_categories = defaultdict(lambda: defaultdict(int))
    no_year_categories = defaultdict(int)

    for entry in entries:
        semester = entry.get('Semester', '')
        cats = entry['Kategorien'].replace('"', '').split('; ')

        if semester:
            # Extract year from semester
            years_found = re.findall(r'20\d{2}', semester)
            if years_found:
                year = years_found[0]  # Take first year found
                for cat in cats:
                    if cat.strip():
                        year_categories[year][cat.strip()] += 1
            else:
                for cat in cats:
                    if cat.strip():
                        no_year_categories[cat.strip()] += 1
        else:
            for cat in cats:
                if cat.strip():
                    no_year_categories[cat.strip()] += 1

    # Get all unique categories
    all_cats = sorted(set(categories.keys()))

    # Create time distribution table
    years_sorted = sorted(year_categories.keys())

    if years_sorted:
        # Header row
        time_header = ['Kategorie'] + years_sorted + ['Laufend']
        time_data = [time_header]

        for cat in all_cats:
            row = [Paragraph(cat, small_style)]
            for year in years_sorted:
                count = year_categories[year].get(cat, 0)
                cell = str(count) if count > 0 else '–'
                row.append(cell)
            # Add "ongoing" column
            ongoing = no_year_categories.get(cat, 0)
            row.append(str(ongoing) if ongoing > 0 else '–')
            time_data.append(row)

        # Calculate column widths
        cat_width = 5*cm
        year_width = 1.2*cm
        col_widths = [cat_width] + [year_width] * (len(years_sorted) + 1)

        time_table = Table(time_data, colWidths=col_widths)
        time_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8e8e8')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))
        story.append(time_table)
        story.append(Spacer(1, 5))
        story.append(Paragraph("<i>Laufend = Lehrveranstaltungen ohne spezifische Semesterangabe</i>", small_style))

    # Add category summary
    story.append(Spacer(1, 20))
    story.append(Paragraph("Kategorien-Übersicht (Gesamt)", category_style))

    cat_data = [['Kategorie', 'Anzahl']]
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        cat_data.append([cat, str(count)])

    cat_table = Table(cat_data, colWidths=[8*cm, 2*cm])
    cat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8e8e8')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ]))
    story.append(cat_table)

    doc.build(story)
    return len(entries)


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    csv_file = project_root / "listen_lv.csv"
    output_dir = project_root / "output" / "files"
    output_file = output_dir / "lehrveranstaltungen.pdf"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    if not csv_file.exists():
        print(f"Error: {csv_file} not found")
        sys.exit(1)

    print(f"Reading {csv_file}...")
    entries = read_csv(csv_file)

    print(f"Found {len(entries)} entries")
    print(f"Generating PDF: {output_file}...")

    count = create_pdf(entries, output_file)

    print(f"Successfully created {output_file} with {count} entries")

    return 0


if __name__ == "__main__":
    sys.exit(main())
