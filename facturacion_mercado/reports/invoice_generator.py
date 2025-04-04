from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_invoice(items, total):
    # Crear directorio de facturas si no existe
    if not os.path.exists('facturas'):
        os.makedirs('facturas')
        
    # Nombre del archivo con fecha y hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"facturas/factura_{timestamp}.pdf"
    
    # Crear PDF
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "MERCADO XYZ")
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 120, "Dirección: Calle Principal 123")
    c.drawString(100, height - 140, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Línea separadora
    c.line(100, height - 150, width - 100, height - 150)
    
    # Detalles de la factura
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 180, "FACTURA")
    
    # Tabla de productos
    y_position = height - 220
    c.setFont("Helvetica-Bold", 10)
    c.drawString(100, y_position, "Producto")
    c.drawString(300, y_position, "Cantidad")
    c.drawString(400, y_position, "Precio Unit.")
    c.drawString(500, y_position, "Subtotal")
    
    y_position -= 20
    c.setFont("Helvetica", 10)
    for item in items:
        c.drawString(100, y_position, item['name'])
        c.drawString(300, y_position, str(item['quantity']))
        c.drawString(400, y_position, item['price'])
        c.drawString(500, y_position, item['subtotal'])
        y_position -= 20
        
    # Total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, y_position - 30, f"TOTAL: {total}")
    
    # Pie de página
    c.setFont("Helvetica", 8)
    c.drawString(100, 50, "Gracias por su compra!")
    c.drawString(100, 40, "Sistema de Facturación Mercado XYZ")
    
    c.save()
    return filename