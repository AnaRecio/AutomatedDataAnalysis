from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "FAANG Investment Report - Q1 2025", 0, 1, "C")
        self.ln(5)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(2)

    def chapter_body(self, body):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 7, body)
        self.ln()

def markdown_to_pdf(md_path):
    pdf = PDF()
    pdf.add_page()

    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("# "):  # Title
            pdf.chapter_title(line.replace("# ", ""))
        elif line.startswith("## "):  # Section
            pdf.chapter_title(line.replace("## ", ""))
        elif line.startswith("### "):  # Subsection
            pdf.chapter_title(line.replace("### ", ""))
        else:
            pdf.chapter_body(line)

    output_path = md_path.replace(".md", ".pdf")
    pdf.output(output_path)
    print(f"📄 PDF generated at: {output_path}")
