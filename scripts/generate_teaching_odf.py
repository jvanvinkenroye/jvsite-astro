#!/usr/bin/env python3
"""
Generate ODF spreadsheet from teaching.md

Parses the teaching.md file and generates an ODF spreadsheet (.ods)
with a structured list of all teaching assignments.
"""

import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from dataclasses import dataclass
from typing import Optional

try:
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.style import Style, TextProperties, TableColumnProperties, ParagraphProperties
    from odf.table import Table, TableColumn, TableRow, TableCell
    from odf.text import P
except ImportError:
    print("Error: odfpy is not installed. Install with: pip install odfpy")
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
    current_category = "Allgemein"

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


def create_odf_spreadsheet(entries: list[TeachingEntry], output_path: Path):
    """Create an ODF spreadsheet from the teaching entries."""
    doc = OpenDocumentSpreadsheet()

    # Create styles
    # Header style
    header_style = Style(name="HeaderStyle", family="table-cell")
    header_style.addElement(TextProperties(fontweight="bold", fontsize="12pt"))
    header_style.addElement(ParagraphProperties(textalign="center"))
    doc.automaticstyles.addElement(header_style)

    # Normal style
    normal_style = Style(name="NormalStyle", family="table-cell")
    normal_style.addElement(TextProperties(fontsize="10pt"))
    doc.automaticstyles.addElement(normal_style)

    # Column styles
    col_styles = {
        'category': ('ColCategory', '3cm'),
        'institution': ('ColInstitution', '5cm'),
        'date': ('ColDate', '2.5cm'),
        'courses': ('ColCourses', '8cm'),
        'degree': ('ColDegree', '5cm'),
    }

    for name, (style_name, width) in col_styles.items():
        col_style = Style(name=style_name, family="table-column")
        col_style.addElement(TableColumnProperties(columnwidth=width))
        doc.automaticstyles.addElement(col_style)

    # Create table
    table = Table(name="Lehraufträge")

    # Add columns
    table.addElement(TableColumn(stylename="ColCategory"))
    table.addElement(TableColumn(stylename="ColInstitution"))
    table.addElement(TableColumn(stylename="ColDate"))
    table.addElement(TableColumn(stylename="ColCourses"))
    table.addElement(TableColumn(stylename="ColDegree"))

    # Add header row
    header_row = TableRow()
    headers = ["Kategorie", "Institution", "Zeitraum", "Lehrveranstaltungen", "Studiengang"]
    for header in headers:
        cell = TableCell(stylename="HeaderStyle")
        cell.addElement(P(text=header))
        header_row.addElement(cell)
    table.addElement(header_row)

    # Add data rows
    for entry in entries:
        row = TableRow()

        # Category
        cell = TableCell(stylename="NormalStyle")
        cell.addElement(P(text=entry.category))
        row.addElement(cell)

        # Institution
        cell = TableCell(stylename="NormalStyle")
        cell.addElement(P(text=entry.institution))
        row.addElement(cell)

        # Date range
        cell = TableCell(stylename="NormalStyle")
        cell.addElement(P(text=entry.date_range))
        row.addElement(cell)

        # Courses (may have multiple lines)
        cell = TableCell(stylename="NormalStyle")
        for line in entry.courses.split('\n'):
            line = line.strip()
            if line:
                cell.addElement(P(text=line))
        row.addElement(cell)

        # Degree program
        cell = TableCell(stylename="NormalStyle")
        cell.addElement(P(text=entry.degree_program or ""))
        row.addElement(cell)

        table.addElement(row)

    doc.spreadsheet.addElement(table)
    doc.save(str(output_path))

    return len(entries)


def main():
    """Main entry point."""
    # Determine paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    teaching_md = project_root / "content" / "pages" / "teaching.md"
    output_dir = project_root / "output" / "files"
    output_file = output_dir / "lehrauftraege.ods"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    if not teaching_md.exists():
        print(f"Error: {teaching_md} not found")
        sys.exit(1)

    print(f"Parsing {teaching_md}...")
    entries = parse_teaching_md(teaching_md)

    print(f"Found {len(entries)} teaching entries")
    print(f"Generating ODF spreadsheet: {output_file}...")

    count = create_odf_spreadsheet(entries, output_file)

    print(f"Successfully created {output_file} with {count} entries")

    return 0


if __name__ == "__main__":
    sys.exit(main())
