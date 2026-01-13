#!/usr/bin/env python3
"""
Generate PDF from teaching.md

Parses the teaching.md file and generates a PDF document
with a structured list of all teaching assignments.
"""

import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from dataclasses import dataclass
from typing import Optional

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
except ImportError:
    print("Error: reportlab is not installed. Install with: pip install reportlab")
    sys.exit(1)


@dataclass
class TeachingEntry:
    """Represents a single teaching assignment entry."""
    category: str
    institution: str
    url: Optional[str]
    date_range: str
    courses: str
    degree_program: Optional[str]


class TeachingEntryParser(HTMLParser):
    """Parse HTML entry blocks from teaching.md."""

    def __init__(self):
        super().__init__()
        self.entries = []
        self.current_entry = {}
        self.current_tag = None
        self.current_class = None
        self.in_entry = False
        self.in_link = False
        self.current_url = None
        self.text_buffer = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_name = attrs_dict.get('class', '')

        if tag == 'div' and class_name == 'entry':
            self.in_entry = True
            self.current_entry = {}

        if self.in_entry:
            if tag == 'span' and class_name in ['entry-title', 'entry-date']:
                self.current_class = class_name
                self.text_buffer = ""
            elif tag == 'div' and class_name == 'entry-description':
                self.current_class = 'entry-description'
                self.text_buffer = ""
            elif tag == 'a' and self.current_class == 'entry-title':
                self.in_link = True
                self.current_url = attrs_dict.get('href', '')
            elif tag == 'em':
                self.current_class = 'degree-program'
                self.text_buffer = ""
            elif tag == 'br':
                self.text_buffer += "\n"

    def handle_endtag(self, tag):
        if tag == 'div' and self.in_entry and self.current_class != 'entry-description':
            if 'institution' in self.current_entry:
                self.entries.append(self.current_entry.copy())
            self.in_entry = False
            self.current_entry = {}

        if self.in_entry:
            if tag == 'span':
                if self.current_class == 'entry-title':
                    self.current_entry['institution'] = self.text_buffer.strip()
                    self.current_entry['url'] = self.current_url
                    self.current_url = None
                elif self.current_class == 'entry-date':
                    self.current_entry['date_range'] = self.text_buffer.strip()
                self.current_class = None
            elif tag == 'div' and self.current_class == 'entry-description':
                self.current_entry['courses'] = self.text_buffer.strip()
                self.current_class = None
            elif tag == 'em':
                self.current_entry['degree_program'] = self.text_buffer.strip()
                self.current_class = None
            elif tag == 'a':
                self.in_link = False

    def handle_data(self, data):
        if self.current_class:
            self.text_buffer += data


def parse_teaching_md(filepath: Path) -> list[TeachingEntry]:
    """Parse teaching.md and extract all teaching entries."""
    content = filepath.read_text(encoding='utf-8')

    # Split by sections
    sections = re.split(r'^### (.+)$', content, flags=re.MULTILINE)

    entries = []

    for i in range(1, len(sections), 2):
        if i < len(sections):
            # Remove HTML tags from category name
            category = re.sub(r'<[^>]+>', '', sections[i]).strip()
            section_content = sections[i + 1] if i + 1 < len(sections) else ""

            # Parse entries in this section
            parser = TeachingEntryParser()
            parser.feed(section_content)

            for entry_data in parser.entries:
                # Clean up courses text - remove degree program if it's in the courses
                courses = entry_data.get('courses', '')
                degree = entry_data.get('degree_program', '')

                # Remove the degree program line from courses if present
                if degree and degree in courses:
                    courses = courses.replace(degree, '').strip()
                    # Clean up trailing newlines and commas
                    courses = re.sub(r'\n+$', '', courses)

                entry = TeachingEntry(
                    category=category,
                    institution=entry_data.get('institution', ''),
                    url=entry_data.get('url'),
                    date_range=entry_data.get('date_range', ''),
                    courses=courses,
                    degree_program=degree
                )
                entries.append(entry)

    return entries


def create_pdf(entries: list[TeachingEntry], output_path: Path):
    """Create a PDF document from the teaching entries."""
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER
    )

    category_style = ParagraphStyle(
        'CategoryStyle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#333333')
    )

    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12
    )

    small_style = ParagraphStyle(
        'SmallStyle',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#666666')
    )

    # Build content
    story = []

    # Title
    story.append(Paragraph("Lehraufträge", title_style))
    story.append(Paragraph("Jan Vanvinkenroye", styles['Normal']))
    story.append(Spacer(1, 20))

    # Group entries by category
    categories = {}
    for entry in entries:
        if entry.category not in categories:
            categories[entry.category] = []
        categories[entry.category].append(entry)

    # Create table for each category
    for category, cat_entries in categories.items():
        story.append(Paragraph(category, category_style))

        # Table data
        table_data = [['Institution', 'Zeitraum', 'Lehrveranstaltungen', 'Studiengang']]

        for entry in cat_entries:
            # Format courses (replace newlines with <br/>)
            courses_formatted = entry.courses.replace('\n', '<br/>')

            table_data.append([
                Paragraph(entry.institution, normal_style),
                Paragraph(entry.date_range, normal_style),
                Paragraph(courses_formatted, normal_style),
                Paragraph(entry.degree_program or '', small_style)
            ])

        # Create table
        col_widths = [4.5*cm, 2.5*cm, 6*cm, 4*cm]
        table = Table(table_data, colWidths=col_widths, repeatRows=1)

        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#333333')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),

            # Body
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),

            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),

            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))

        story.append(table)
        story.append(Spacer(1, 15))

    doc.build(story)
    return len(entries)


def main():
    """Main entry point."""
    # Determine paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    teaching_md = project_root / "content" / "pages" / "teaching.md"
    output_dir = project_root / "output" / "files"
    output_file = output_dir / "lehrauftraege.pdf"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    if not teaching_md.exists():
        print(f"Error: {teaching_md} not found")
        sys.exit(1)

    print(f"Parsing {teaching_md}...")
    entries = parse_teaching_md(teaching_md)

    print(f"Found {len(entries)} teaching entries")
    print(f"Generating PDF: {output_file}...")

    count = create_pdf(entries, output_file)

    print(f"Successfully created {output_file} with {count} entries")

    return 0


if __name__ == "__main__":
    sys.exit(main())
