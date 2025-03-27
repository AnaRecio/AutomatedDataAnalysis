from fpdf import FPDF
import os
import re
from datetime import datetime

# Directory where custom fonts are stored
FONT_DIR = "assets/fonts"

class InvestmentPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

        # Register custom DejaVu fonts for full Unicode support
        self.add_font("DejaVu", "", os.path.join(FONT_DIR, "DejaVuSans.ttf"), uni=True)
        self.add_font("DejaVu", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), uni=True)
        self.add_font("DejaVu", "I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf"), uni=True)
        self.add_font("DejaVu", "BI", os.path.join(FONT_DIR, "DejaVuSans-BoldOblique.ttf"), uni=True)

    def header(self):
        # PDF header shown on every page
        self.set_font("DejaVu", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, "FAANG Investment Report — Q1 2025", 0, 1, "C", fill=True)
        self.ln(5)

    def footer(self):
        # Footer with page number and generation date
        self.set_y(-15)
        self.set_font("DejaVu", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d')} — Page {self.page_no()}", 0, 0, "C")

    def write_title(self, title):
        # Write document title
        self.set_font("DejaVu", "B", 14)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 10, title)
        self.ln(4)

    def write_section(self, title):
        # Write section headers
        self.set_font("DejaVu", "B", 12)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 8, title)
        self.ln(2)

    def write_text(self, body):
        # Write standard paragraph text
        self.set_font("DejaVu", "", 10)
        self.set_text_color(0)
        self.multi_cell(0, 6, body)
        self.ln(1)

    def write_bullet(self, line):
        # Write bulleted list item
        self.set_font("DejaVu", "", 10)
        self.cell(5, 5, u"\u2022")
        self.multi_cell(0, 5, line.strip())
        self.ln(1)

    def write_table_row(self, columns):
        # Write a single row in a generic table
        self.set_font("DejaVu", "", 10)
        for col in columns:
            self.cell(40, 8, col.strip(), border=1)
        self.ln()

    def write_markdown_table(self, header, rows):
        # Renders a markdown-style table from headers and row data
        col_widths = [35, 30, 40, 30, 30, 30] 
        self.set_font("DejaVu", "B", 10)
        for i, col in enumerate(header):
            self.cell(col_widths[i], 8, col, border=1, align="C")
        self.ln()
        self.set_font("DejaVu", "", 10)
        for row in rows:
            for i, col in enumerate(row):
                self.cell(col_widths[i], 8, col, border=1)
            self.ln()
        self.ln(5)

def markdown_to_pdf(md_path: str):
    """
    Converts a markdown report to a styled PDF using InvestmentPDF class.

    Args:
        md_path (str): Path to the markdown (.md) file
    """
    pdf = InvestmentPDF()
    pdf.add_page()

    # Read markdown content
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Parse markdown line-by-line
    lines_iter = iter(lines)
    for line in lines_iter:
        line = line.strip()

        if line.startswith("# "):
            pdf.write_title(line[2:])
        elif line.startswith("## "):
            pdf.write_section(line[3:])
        elif line.startswith("### "):
            pdf.write_section(line[4:])
        elif line.startswith("- "):
            pdf.write_bullet(line[2:])
        elif "|" in line:
            # Handle markdown tables (requires at least 2 lines: headers and --- row)
            next_line = next(lines_iter, "").strip()
            if "---" in next_line:
                table_lines = [line, next_line]
                for table_row in lines_iter:
                    if "|" not in table_row:
                        break
                    table_lines.append(table_row.strip())
                if len(table_lines) >= 2:
                    headers = [h.strip() for h in table_lines[0].split("|") if h.strip()]
                    rows = [
                        [cell.strip() for cell in row.split("|") if cell.strip()]
                        for row in table_lines[2:]
                    ]
                    pdf.write_markdown_table(headers, rows)
            else:
                # Fallback to plain text for malformed tables
                pdf.write_text(line)
                if next_line:
                    pdf.write_text(next_line)
        elif line:
            pdf.write_text(line)

    # Embed stock chart if available
    chart_path = "charts/stock_prices.png"
    if os.path.exists(chart_path):
        pdf.add_page()
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "Stock Price Comparison", 0, 1, "C")
        pdf.image(chart_path, x=25, y=None, w=160)

    # Export final PDF
    output_path = md_path.replace(".md", ".pdf")
    pdf.output(output_path)
    print(f"PDF report generated at: {output_path}")

