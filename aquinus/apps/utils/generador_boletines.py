from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
import os
from datetime import datetime

from django.db.models import Avg
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from django.conf import settings
from apps.cursos.models import Asignatura, Calificaciones, Cursante
from .conversorPalacios import convertirEspecialidad, convertirOrientaciones, convertirGrado
from apps.alumnos.models import persona
from apps.calificaciones.views import obtenerCalificacionesAnual, obtenerCalificacionesTrimestral,obtenerCalificacionesSemestral,obtenerCalificacionesCuatrimestral
from .rotated_text import verticalText

# Registro de cada estilo de la fuente
font_path = os.path.join(settings.BASE_DIR, 'static', 'assets','fonts','lato')  # Ruta de la carpeta de fuentes
pdfmetrics.registerFont(TTFont('Lato', os.path.join(font_path, 'Lato-Black.ttf')))
pdfmetrics.registerFont(TTFont('LatoBd', os.path.join(font_path, 'Lato-Bold.ttf')))
# Definir la familia de fuentes "Vera"
registerFontFamily('Lato', normal='Lato', bold='LatoBd')


def generate_header(canvas, doc):
    """
    Función para dibujar el encabezado centrado en cada página del documento.
    """
    alumno = getattr(doc, 'alumno', None)
    styles = getSampleStyleSheet()
    header_style = styles["Heading1"]
    header_style.alignment = 1  # Centrar el encabezado
    
    # Ruta de la imagen
    image_path = os.path.join(settings.BASE_DIR, 'static', 'assets', 'images', 'boletin', 'heraldica.png')
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Imagen no encontrada en la ruta: {image_path}") 
    
    # Dimensiones de la página
    page_width, page_height = doc.pagesize
    
    # Guardar el estado de la página antes de modificarla
    canvas.saveState()

    # Dibujar imagen centrada (ajustar el tamaño si es necesario)
    image_width = 60
    image_height = 60
    canvas.setFillColor(colors.lightblue, alpha=0.3)  # Fondo azul claro
    canvas.setStrokeColor(colors.lightblue)  # Sin borde, usa el mismo color del fondo

    # Dibujar el rectángulo de fondo
    canvas.rect(20, page_height - image_height - 15, 
        page_width - 40, image_height + 5, 
        fill=1)  # fill=1 para rellenar el fondo
    canvas.setFillColor(colors.blue)
    canvas.drawImage(image_path, ( image_width) / 2, page_height - image_height - 15, width=image_width, height=image_height, mask="auto")
    
    # Dibujar título centrado
    canvas.setFont("Lato", 18)
    
    canvas.drawCentredString(page_width/3.5, page_height -50, "Escuela de Suboficiales de la Armada")
    
    # Dibujar texto centrado
    canvas.setFont("Lato", 12)
    canvas.drawCentredString(page_width / 3.5, page_height - 65, "Boletín de Calificaciones")
    
    
    # Añadir línea horizontal debajo del encabezado
    canvas.setStrokeColor(colors.blue)
    canvas.setLineWidth(1)
    canvas.line(20, page_height - image_height - 15, page_width - 20, page_height - image_height - 15)  # Línea horizontal
    canvas.line(20, page_height -10, page_width - 20, page_height -10)  # Línea horizontal
    canvas.line(page_width/2,page_height-10,page_width/2, page_height - image_height - 15)  # Línea vertical
    canvas.line(20,page_height-10,20, page_height - image_height - 15)  # Línea vertical
    canvas.line(page_width - 20,page_height-10,page_width - 20, page_height - image_height - 15)  # Línea vertical
    
    canvas.setFont("Lato", 10)
    canvas.drawString(page_width / 2+10, page_height - 25, "Apellido y Nombre:")
    canvas.drawString(page_width / 2+10, page_height - 37, "Grado:")
    canvas.drawString(page_width / 2+10, page_height - 49, "Especialidad:")
    canvas.drawString(page_width / 2+10, page_height - 61, "Orientacion:")
    canvas.drawString(page_width / 2+220, page_height - 37, "M.R.:")
    canvas.setFont("Lato", 12)
    canvas.drawString(page_width / 2+105, page_height - 25, f'{alumno.apellidos}, {alumno.nombres}')
    canvas.drawString(page_width / 2+105, page_height - 37, f'{convertirGrado(alumno.grado)}')
    canvas.drawString(page_width / 2+105, page_height - 49, f'{convertirEspecialidad(alumno.especialidad)}')
    canvas.drawString(page_width / 2+105, page_height - 61, f'{convertirOrientaciones(alumno.orientacion)}')
    canvas.drawString(page_width / 2+260, page_height - 37, f'{alumno.mr}')
    
    # Restaurar el estado del canvas
    canvas.restoreState()


def generate_footer(canvas, doc):
    """
    Función para generar el pie de página.
    """
    # Fecha y hora actual
    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Define el texto del pie de página
    footer_text = f"Página {doc.page}"
    page_width, page_height = doc.pagesize

    # Dibujar la línea horizontal del pie de página
    canvas.setStrokeColor(colors.blue)
    canvas.setLineWidth(1)
    canvas.line(30, 40, page_width - 30, 40)  # Línea horizontal

    # Configuración de fuente y color para el pie de página
    canvas.setFont("Lato", 10)

    # Fecha y hora en el margen izquierdo
    canvas.setFillColor(colors.black)
    canvas.drawString(30, 20, f"Generado el: {current_datetime}")

    # Texto centrado para la numeración de páginas
    canvas.drawCentredString(page_width / 2, 15, footer_text)

    # Marca en el margen derecho
    canvas.setFillColor(colors.grey)
    canvas.drawString(page_width - 130, 20, "Aquinus by P.P. - 2024")



def generate_header_footer(canvas, doc):
    generate_header(canvas, doc)
    makeWatermark(canvas, doc)
    generate_footer(canvas, doc)



def makeWatermark(c, doc):
    text = "AQUINUS"
    image_path = os.path.join(settings.BASE_DIR, 'static', 'assets', 'images', 'aquinus-logo-2.png')
    
    # Verifica que la imagen exista
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Imagen no encontrada en la ruta: {image_path}")
    # Dimensiones de la página
    page_width, page_height = doc.pagesize
    # Configura el centro de la página para la marca de agua
    center_x =  page_width/ 2
    center_y = page_height / 2
    
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



def generar_boletin_pdf(request, pk):
    # Crear el documento PDF
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
    page_size = landscape(A4)
    doc = SimpleDocTemplate(response, pagesize=page_size, topMargin=2.5*cm, bottomMargin=1.5*cm, leftMargin=0.5*cm, rightMargin=0.5*cm)
    elements = []
    alumno = get_object_or_404(persona.objects.using('id8'), dni=pk)
    # Pasar el objeto del alumno al documento
    doc.alumno = alumno  # Agregamos el alumno como un atributo dinámico
    
    
    # Datos de ejemplo para la tabla
    # data = [
    #     ['', 'Materia', '1er. Trim.', '2do. Trim.', '3er. Trim.', 'Nota Cursada', 'Ex. Final', 'Nota Final'],
    #     [verticalText("ANUALES"), 'Análisis Matemático', 5, 8, 4, 7, 7, 7],
    #     ['', 'Lenguaje', 5, 8, 4, 5, 7, 7],
    #     ['', 'Álgebra aplicada', 5, 8, 4, 7, 7, 7],
    #     [vertic
    data,cant_anuales,cant_trimestrales,cant_semestrales=obtener_calificaciones_tipo_trimestrales(alumno)
   
    data_bimestrales=obtener_calificaciones_tipo_bimestrales(alumno)
    print("DATA BIMESTRALES EN EL GENERAR BOELTIN", data_bimestrales)
    # data_bimestrales = [
    #     ['', 'Materia', '1er. Bim.', '2do. Bim.', '3er. Bim.', '4to. Bim.','Nota Cursada', 'Ex. Final', 'Nota Final'],
    #     [verticalText("CUATRIM."), 'Botánica', 5, 8, '','', 5, 7, 7],
    #     ['', 'Física', 5, 8, '','', 5, 7, 7],
      
        
        
    # ]
    num_columns = len(data[0])  # Basado en la primera fila
    num_columns_bimestrales = len(data_bimestrales[0])
# Crear una lista dinámica de anchos
    col_widths = [20] + [None] * (num_columns - 1)  # Primera columna fija, las demás automáticas
    col_widths_bimestrales = [20] + [None] * (num_columns_bimestrales - 1)
    # Detectar los rangos dinámicamente
    # rangos = {}
   
    # current_section = None

    # for idx, row in enumerate(data):
    #     # Si la primera columna tiene texto, inicia una nueva sección
    #     if row[0] and row[0] != '':
    #         current_section = row[0]
    #         rangos[current_section] = [idx, idx]  # Inicia el rango con la fila actual
    #     elif current_section:
    #         # Si estamos en una sección, expandir el rango
    #         rangos[current_section][1] = idx
            
            
    rangos_bimestrales = {}
    current_section = None
    
    for idx, row in enumerate(data_bimestrales):
        # Si la primera columna tiene texto, inicia una nueva sección
        if row[0] and row[0] != '':
            current_section = row[0]
            rangos_bimestrales[current_section] = [idx, idx]  # Inicia el rango con la fila actual
        elif current_section:
            # Si estamos en una sección, expandir el rango
            rangos_bimestrales[current_section][1] = idx
    

    # Crear la tabla
    table = Table(data,colWidths=col_widths)
    tabla_bimestrales=Table(data_bimestrales, colWidths=col_widths_bimestrales)
    # Aplicar estilo a la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROUNDEDCORNERS', [3, 3, 3,3]),
         ('VALIGN',(0,0),(0,-1),'MIDDLE'),
         ('BACKGROUND', (0, 0), (0, -1), colors.grey),  # primera celda
         ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('SPAN', (0, 1), (0, cant_anuales)),
        ('SPAN', (0, cant_anuales+1), (0, cant_trimestrales+cant_anuales)),
        ('SPAN', (0, cant_trimestrales+cant_anuales+1), (0, -1)),
         
    ])
    style_bimestrales= TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
          ('ROUNDEDCORNERS', [3, 3, 3,3])
    ])
    # Aplicar spans basados en los rangos detectados
    # for section, (start, end) in rangos.items():
    #     style.add('SPAN', (0, start), (0, end))  # Hacer el span para la primera columna
     # Aplicar spans basados en los rangos detectados
    for section, (start, end) in rangos_bimestrales.items():
        style_bimestrales.add('SPAN', (0, start), (0, end))  # Hacer el span para la primera columna
        
    # Agregar fondo a las celdas vacías
    for row_idx, row in enumerate(data[1:], start=1):  # Excluir encabezado
        for col_idx, cell in enumerate(row):
            if col_idx != 0 and cell == "":  # Excluir la primera columna
                style.add('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.lightgrey)
    # Agregar fondo a las celdas vacías
    for row_idx, row in enumerate(data_bimestrales[1:], start=1):  # Excluir encabezado
        for col_idx, cell in enumerate(row):
            if col_idx != 0 and cell == "":  # Excluir la primera columna
                style_bimestrales.add('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.lightgrey)
    table.setStyle(style)
    tabla_bimestrales.setStyle(style_bimestrales)
    # Agregar la tabla al documento
    elements.append(Spacer(1, 12))
    elements.append(table)
    elements.append(PageBreak())
    elements.append(Spacer(1, 12))
    elements.append(tabla_bimestrales)
    # Generar el PDF
    doc.build(elements, onFirstPage=generate_header_footer, onLaterPages=generate_header_footer)

    return response


def obtener_calificaciones_tipo_trimestrales(alumno):
    cursante=Cursante.objects.get(dni=alumno.dni)
    materias_con_calificaciones_anuales = {}
    materias_con_calificaciones_trimestrales={}
    materias_con_calificaciones_semestrales={}
    asignaturas_anuales=Asignatura.objects.filter(curso=cursante.curso, materia__tipo="ANUAL")   
    asignaturas_semestrales=Asignatura.objects.filter(curso=cursante.curso, materia__tipo="SEMESTRAL")
    asignaturas_trimestrales=Asignatura.objects.filter(curso=cursante.curso, materia__tipo="TRIMESTRAL") 
    cantidad_anuales=len(asignaturas_anuales)
    cantidad_semestrales=len(asignaturas_semestrales)
    cantidad_trimestrales=len(asignaturas_trimestrales)
    for asignatura in asignaturas_anuales:
            materias_con_calificaciones_anuales[asignatura]=obtenerCalificacionesAnual(asignatura, alumno)
    
     
    #Encabezado de la tabla    
    data_anuales=[['', 'Materia', '1er. Trim.', '2do. Trim.', '3er. Trim.', 'Nota Cursada', 'Ex. Final', 'Nota Final'],]
    
    #información de materias anuales
    for indice, (asignatura, calificaciones) in enumerate(materias_con_calificaciones_anuales.items()):  
        data_materia=[ asignatura.materia.nombre]
        if indice==0:
                data_materia.insert(0,verticalText("Anuales"))
        else:
            data_materia.insert(0,"")
        for  k,v in calificaciones.items():
            
            if k in ['promedio_1T', 'promedio_2T', 'promedio_3T', 'promedio_cursada', 'examen_final', 'calificacion_final']:
                if k=='examen_final':
                    if  not isinstance(v, Calificaciones)and v['valor']=='Sin Calificación' :                   
                        data_materia.append('Sin Calificar')
                    else:
                        data_materia.append(v.valor)
                else:                  
                    data_materia.append(v)
              
                
        data_anuales.append(data_materia)
        
    #información de materias trimestrales   
    for asignatura in asignaturas_trimestrales:
        materias_con_calificaciones_trimestrales[asignatura]=obtenerCalificacionesTrimestral(asignatura, alumno) 
         
    for indice, (asignaturas, calificaciones) in enumerate(materias_con_calificaciones_trimestrales.items()):
        data_materia_trimestrales=[asignaturas.materia.nombre]  
        if indice==0:
                data_materia_trimestrales.insert(0,verticalText("Trimestrales"))
        else:
            data_materia_trimestrales.insert(0,"")
        for k,v in calificaciones.items():
            
            if v==0:
                valor=""
            else:
                valor=v
            if k =="promedio_T":
                if asignatura.periodo_cursado==1:
                    data_materia_trimestrales.insert(2,valor)
                    data_materia_trimestrales.insert(3,"")
                    data_materia_trimestrales.insert(4,"")
                elif asignatura.periodo_cursado==2:
                    data_materia_trimestrales.insert(3,valor)
                    data_materia_trimestrales.insert(2,"")
                    data_materia_trimestrales.insert(4,"")
                elif asignatura.periodo_cursado==3:
                    data_materia_trimestrales.insert(4,valor)
                    data_materia_trimestrales.insert(3,"")
                    data_materia_trimestrales.insert(2,"")
                data_materia_trimestrales.insert(5,valor)      
            elif k=="promedio_cursada":
                data_materia_trimestrales.insert(6,valor)
            elif k=="examen_final":
                data_materia_trimestrales.insert(7,valor['valor'])
            elif k=="calificacion_final":
                data_materia_trimestrales.insert(8,valor)  
                    
        data_anuales.append(data_materia_trimestrales)     
        
    #información de materias semestrales
    for asignatura in asignaturas_semestrales:
        materias_con_calificaciones_semestrales[asignatura]=obtenerCalificacionesSemestral(asignatura, alumno)
    for indice,(asignaturas, calificaciones) in enumerate(materias_con_calificaciones_semestrales.items()):
        if indice==0:
            
            data_materia_semestrales=[verticalText("Sem."),asignatura.materia.nombre, "", "", "", "", "",""]
        else:
            data_materia_semestrales=["",asignatura.materia.nombre, "", "", "", "", "",""]
        #data_materia_semestrales.insert(0,"")
        for k,v in calificaciones.items():
         
            if v==0:
                valor=""
            else:
                valor=v
            if k=="promedio_1T":
                data_materia_semestrales[2]=valor
                    
            elif k=="promedio_2T":
                data_materia_semestrales[3]=valor
            elif k=="promedio_3T":
                data_materia_semestrales[4]=valor
            elif k=="promedio_cursada":
                data_materia_semestrales[5]=valor
            elif k=="examen_final":
                data_materia_semestrales[6]=valor['valor']
            elif k=="calificacion_final":
                data_materia_semestrales[7]=valor
        data_anuales.append(data_materia_semestrales)
        
    # for asignatura,calificaciones in materias_con_calificaciones_trimestrales.items():
    #     print("ASIGNATURA ",asignatura, " CALIFICACIONES", calificaciones) 
    return data_anuales,cantidad_anuales,cantidad_trimestrales,cantidad_semestrales
    
    
def obtener_calificaciones_tipo_bimestrales(alumno):
    cursante=Cursante.objects.get(dni=alumno.dni)
    materias_con_calificaciones_cuatrimestrales = {}
    materias_con_calificaciones_bimestrales={}

    asignaturas_bimestrales=Asignatura.objects.filter(curso=cursante.curso, materia__tipo="BIMESTRAL")   
    asignaturas_cuatrimestrales=Asignatura.objects.filter(curso=cursante.curso, materia__tipo="CUATRIMESTRAL")
    
    
    for asignatura in asignaturas_cuatrimestrales:
            materias_con_calificaciones_cuatrimestrales[asignatura]=obtenerCalificacionesCuatrimestral(asignatura, alumno)
    
     
    #Encabezado de la tabla    
    data_tabla_bimestral=[ ['', 'Materia', '1er. Bim.', '2do. Bim.', '3er. Bim.', '4to. Bim.','Nota Cursada', 'Ex. Final', 'Nota Final'],]
    
    for indice,(asignaturas, calificaciones) in enumerate(materias_con_calificaciones_cuatrimestrales.items()):
        if indice==0:
            
            data_cuatrimestrales=[verticalText("Cuatrim."),asignaturas.materia.nombre, "", "", "", "", "","",""]
        else:
            data_cuatrimestrales=["",asignaturas.materia.nombre, "", "", "", "", "","",""]
        #data_materia_semestrales.insert(0,"")
        for k,v in calificaciones.items():
         
            if v==0:
                valor=""
            else:
                valor=v
            if k=="promedio_1B":
                data_cuatrimestrales[2]=valor
                    
            elif k=="promedio_2B":
                 data_cuatrimestrales[3]=valor
            elif k=="promedio_3B":
                 data_cuatrimestrales[4]=valor
            elif k=="promedio_4B":
                 data_cuatrimestrales[5]=valor
            elif k=="promedio_cursada":
                data_cuatrimestrales[6]=valor
            elif k=="examen_final":
                data_cuatrimestrales[7]=valor
            elif k=="calificacion_final":
                data_cuatrimestrales[8]=valor
        data_tabla_bimestral.append(data_cuatrimestrales)

    return data_tabla_bimestral