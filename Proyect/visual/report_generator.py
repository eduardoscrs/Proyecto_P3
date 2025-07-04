from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf_report(filename: str, content: str):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter  # Tamaño de la página

    # Escribir contenido en el PDF
    c.drawString(100, height - 100, content)

    # Guardar el archivo PDF
    c.save()

    print(f"PDF generado: {filename}")
