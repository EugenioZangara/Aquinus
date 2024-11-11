import os
from django.conf import settings
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily



# Registro de cada estilo de la fuente
font_path = os.path.join(settings.BASE_DIR, 'static', 'assets','fonts','lato')  # Ruta de la carpeta de fuentes
pdfmetrics.registerFont(TTFont('Lato', os.path.join(font_path, 'Lato-Black.ttf')))
pdfmetrics.registerFont(TTFont('LatoBd', os.path.join(font_path, 'Lato-Bold.ttf')))
# Definir la familia de fuentes "Vera"
registerFontFamily('Lato', normal='Lato', bold='LatoBd')

# Definir la familia de fuentes "Vera"



PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)
styles = getSampleStyleSheet()
Title = "ESCUELA DE SUBOFICIALES DE LA ARMADA"
SubTitle = "Boletín de Calificaciones del Aspirante:"
pageinfo = "Aquinus - P.P."

# Dummy data for the table (replace with your actual data)
data = [
    ["Materia", "1er Trim.", "2do Trim.", "3er Trim.", "Nota Cursada", "Examen Final", "Nota Final"],
    ["Matemáticas", "7", "8", "9", "8", "8", "8"],
    ["Física", "6", "6", "7", "6.3", "7", "6.5"],
    ["Química", "8", "7", "9", "8", "8", "8"],
    ["Álgebra", "7", "8", "9", "8", "8", "8"],
    ["Historia", "6", "6", "7", "6.3", "7", "6.5"],
    ["Pintura", "8", "7", "9", "8", "8", "8"],
    ["Biología", "7", "7", "8", "7.3", "7", "7.2"],
    ["Geografía", "8", "8", "9", "8.3", "8", "8.2"],
    ["Música", "7", "9", "8", "8", "9", "8.5"],
    ["Tecnología", "6", "6", "7", "6.3", "7", "6.5"],
    ["Educación Física", "9", "9", "10", "9.3", "9", "9.2"],
    ["Literatura", "7", "8", "8", "7.7", "8", "7.8"],
    ["Idiomas", "8", "7", "8", "7.7", "8", "7.8"],
]
data_semestrales = [
    ["Materia", "1er Trim.", "2do Trim.", "3er Trim.", "Nota Cursada", "Examen Final", "Nota Final"],
    ["Filosofía", "7", "8", "", "7.5", "5", "6.3"],
    ["Sociología", "6", "7", "", "6.5", "6", "6.2"],
    ["Economía", "8", "7", "", "7.5", "7", "7.2"],
    ["Antropología", "9", "8", "", "9.5", "8", "9.3"],
]
data_trimestrales = [
    ["Materia", "1er Trim.", "2do Trim.", "3er Trim.", "Nota Cursada", "Examen Final", "Nota Final"],
    ["Historia", "7", "", "", "7.5", "6", "6.8"],
   ["Geografía", "6", "", "", "6.5", "6", "6.2"],
]
data_cuatrimestrales = [
    ["Materia", "1er Bim.", "2do Bim.", "Nota Cursada", "Examen Final", "Nota Final"],
    ["Filosofía", "7", "8",  "7.5", "5", "6.3"],
    ["Sociología", "6", "7", "6.5", "6", "6.2"],
    ["Economía", "8", "7",  "7.5", "7", "7.2"],
    ["Antropología", "9", "8",  "9.5", "8", "9.3"],
]

def draw_header(c, aspirante="ANPA Juan PEREZ"):
    image_path = os.path.join(settings.BASE_DIR, 'static', 'assets', 'images', 'boletin', 'heraldica.png')
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Imagen no encontrada en la ruta: {image_path}") 
    c.saveState()
    c.setFillColor(colors.white)
    c.setFillAlpha(0.5)
    c.setStrokeColor(colors.blue)
    c.rect(10, PAGE_HEIGHT - 85, PAGE_WIDTH-20, 70, fill=1)
    c.restoreState()
    c.setFont("Times-Bold", 20)
    c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 50, Title)
    c.setFont("Times-Bold", 16)
    c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 70, SubTitle + " " + aspirante)
    c.drawImage(
        image_path,
        0,
        PAGE_HEIGHT - 90,
        width=80,
        height=80,
        mask="auto",
    )
    c.setStrokeColor(colors.blue)
    c.setFont("Times-Bold", 10)
    #c.drawString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 100, "Año: Primer Año - Especialidad: Aeronáutico - Orientación: Supervivencia - Ciclo Lectivo: 2024 - División: 1" )
    c.drawString(15, PAGE_HEIGHT-100, "Apellido y Nombre: Juan PEREZ")
    c.drawString(15, PAGE_HEIGHT-110, "M.R.: 11155454")
    
    c.drawString((PAGE_WIDTH/3)+15, PAGE_HEIGHT-100, "Año: Primer Año")
    c.drawString((PAGE_WIDTH/3)+15, PAGE_HEIGHT-110, "Ciclo Lectivo: 2024")
    c.drawString((PAGE_WIDTH*2/3)+15, PAGE_HEIGHT-100, "Especialidad: Aeronáutico")
    c.drawString((PAGE_WIDTH*2/3)+15, PAGE_HEIGHT-110, "Orientación: Supervivencia")
    
    
    
    
    c.line(10, PAGE_HEIGHT - 120, PAGE_WIDTH - 10, PAGE_HEIGHT - 120)

def draw_footer(p, page_number):
    p.setFont("Helvetica", 10)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(60, 30, f"Página {page_number}")
    p.setFillColor(colors.grey, alpha=0.3)
    p.drawString(PAGE_WIDTH-130, 20, "Aquinus by P.P. - 2024 ")

def draw_anuales(c,data):
    table_data=[[""] + data[0]] + [["ANUALES"] + row for row in data[1:]]
    color="lightsalmon"
    offset_y_inicial_tablas=  PAGE_HEIGHT - 140
    fixed_y=draw_table(c, table_data, color, offset_y_inicial_tablas)
    return fixed_y
    
def draw_semestrales(c,data):
    table_data=[[""] + data[0]] + [["SEMESTRALES"] + row for row in data[1:]]
    color="lightblue"
    offset_y_inicial_tablas=  PAGE_HEIGHT - 140
    draw_table(c, table_data, color, offset_y_inicial_tablas)
    
def draw_trimestrales(c,data):
    table_data=[[""] + data[0]] + [["TRIMESTRALES"] + row for row in data[1:]]
    color="lightgreen"
    offset_y_inicial_tablas=  PAGE_HEIGHT - 140
    draw_table(c, table_data, color, offset_y_inicial_tablas)
    
def draw_cuatrimestrales(c, data, fixed_y):
    table_data=[[""] + data[0]] + [["CUATRIMESTRALES"] + row for row in data[1:]]
    color="lightskyblue"
    offset_y_inicial_tablas=  fixed_y
    draw_table(c, table_data, color, offset_y_inicial_tablas)
    


def draw_table(c, data, color, y_offset):
    table = Table(data, colWidths=[100, 80] + [80] * 5)  # Ajusta colWidths según el nuevo formato

    x_offset = 100
    y_offset =y_offset  # Posición fija del borde superior izquierdo
    color_fondo = getattr(colors, color, colors.white)  # Usar un color predeterminado si no se encuentra el color
    # Define el estilo base de la tabla
    table_style = TableStyle([
        ('ROUNDEDCORNERS', (0, 0), (-1, -1), 3),
         ('SPAN', (0, 1), (0, -1)),  # Expandir "ANUALES" en la primera columna desde la segunda fila hasta la última
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Fondo gris para el encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), color_fondo),  # Fondo beige para el resto de la tabla
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Bordes de las celdas
    ])

    # Agrega el color de fondo para las celdas vacías
    for row_idx, row in enumerate(data[1:], start=1):  # Excluir encabezado
        for col_idx, cell in enumerate(row):
            if cell == "":
                table_style.add('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.lightgrey)

    # Aplicar estilos a la tabla
    table.setStyle(table_style)

    # Calcula el tamaño de la tabla sin dibujarla aún
    table_width, table_height = table.wrap(PAGE_WIDTH, PAGE_HEIGHT)
    
    # Ajusta y_offset para que el borde superior izquierdo permanezca fijo
    fixed_y_offset = y_offset - table_height

    # Dibuja la tabla en las coordenadas especificadas con el y_offset ajustado
    table.drawOn(c, x_offset, fixed_y_offset)
    return fixed_y_offset

def generar_boletin_pdf(request):
    width = PAGE_WIDTH
    height = PAGE_HEIGHT
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="boletin.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=(width, height))
    
    draw_header(p, "PEREZ, Juan")
   
    fixed_y_cuatrimestrales= draw_anuales(p, data)-10  # Llamada para dibujar la tabla en el PDF
    draw_semestrales(p, data_semestrales)  # Llamada para dibujar la tabla en el PDF
    draw_trimestrales(p, data_trimestrales)  # Llamada para dibujar la tabla en el PDF
    draw_cuatrimestrales(p, data_cuatrimestrales, fixed_y_cuatrimestrales)  # Llamada para dibujar la tabla en el PDF
    
    draw_footer(p, 1)
    makeWatermark(p)
    p.showPage()
    
    # Segunda página
    draw_header(p, "PEREZ, Juan - Continuación")
    draw_footer(p, 2)
    p.save()
    
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def makeWatermark(c):
    text = "AQUINUS"
    image_path = os.path.join(settings.BASE_DIR, 'static', 'assets', 'images', 'aquinus-logo-2.png')
    
    # Verifica que la imagen exista
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Imagen no encontrada en la ruta: {image_path}")
    
    # Configura el centro de la página para la marca de agua
    center_x = PAGE_WIDTH / 2
    center_y = PAGE_HEIGHT / 2
    
    # Define tamaño del texto y la imagen
    text_size = 100
    image_width, image_height = 150,150  # Ajusta el tamaño según sea necesario
    
    # Guarda el estado actual de la página
    c.saveState()
    
    # Coloca la marca de agua con un color gris claro y un ángulo de 30 grados
    c.setFillColor(colors.grey, alpha=0.3)
    c.setFont("Lato", text_size)
    
    # Traslada al centro de la página
    c.translate(center_x, center_y)
    c.rotate(30)  # Rota la marca de agua
    
    # Dibuja el texto centrado en el nuevo origen
    c.drawCentredString(0, 0, text)
    
    # Calcula la posición de la imagen a la derecha del texto
    text_width = c.stringWidth(text, "Lato", text_size)  # Ancho del texto en puntos
    image_x = -350  # 10 es un margen opcional
    
    # Dibuja la imagen alineada con el texto
    c.drawImage(
        image_path,
        image_x, -text_size/3,  # Alinea verticalmente al centro del texto
        width=image_width,
        height=image_height,
        mask="auto"
    )
    
    # Restaura el estado anterior de la página
    c.restoreState()
