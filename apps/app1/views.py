from django.db import transaction
from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.core import serializers
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from .models import *
from .forms import *
from io import BytesIO
import time


# Vista para el menu de inicio
def index(request):
    return render(
        request,
        'base/base.html',
    )

#-----------------------------------------------------------------------------------------------

def consultaCiclo(request):
    ciclo_list=Ciclo.objects.order_by('codigo_ciclo')
    context = {
        'ciclo_list': ciclo_list,
    }
    return render(
        request,
        'app1/Ciclo.html', context
    )

class crearCiclo(CreateView):
    template_name = 'app1/crear_ciclo.html'
    form_class = CicloForm
    success_url = reverse_lazy('proyeccionsocial:consulta_ciclo')

class editarCiclo(UpdateView):
    model = Ciclo
    template_name = 'app1/crear_ciclo.html'
    form_class = CicloForm
    success_url = reverse_lazy('proyeccionsocial:consulta_ciclo')

class eliminarCiclo(DeleteView):
    model = Ciclo
    template_name = 'app1/eliminar_ciclo.html'
    success_url = reverse_lazy('proyeccionsocial:consulta_ciclo')

#-----------------------------------------------------------------------------------------------

def consultaEstudiante(request):
    estudiante_list=Estudiante.objects.order_by('carnet_estudiante')
    context = {
        'estudiante_list': estudiante_list,
    }
    return render(
        request,
        'app1/Estudiante.html', context
    )

class crearEstudiante(CreateView):
    template_name = 'app1/crear_estudiante.html'
    form_class = EstudianteForm
    success_url = reverse_lazy('proyeccionsocial:consulta_estudiante')

class editarEstudiante(UpdateView):
    model = Estudiante
    template_name = 'app1/crear_estudiante.html'
    form_class = EstudianteForm
    success_url = reverse_lazy('proyeccionsocial:consulta_estudiante')

class eliminarEstudiante(DeleteView):
    model = Estudiante
    template_name = 'app1/eliminar_estudiante.html'
    success_url = reverse_lazy('proyeccionsocial:consulta_estudiante')

#-----------------------------------------------------------------------------------------------


def consultaEstudioUniversitario(request):
    estudios_list=EstudioUniversitario.objects.order_by('codigo_carrera')
    context = {
        'estudios_list': estudios_list,
    }
    return render(
        request,
        'app1/EstudioUniversitario.html', context
    )

class crearEstudioUniversitario(CreateView):
    template_name = 'app1/crear_estudio_universitario.html'
    form_class = EstudioUniversitarioForm
    success_url = reverse_lazy('proyeccionsocial:consulta_estudio_universitario')

class editarEstudioUniversitario(UpdateView):
    model = EstudioUniversitario
    template_name = 'app1/crear_estudio_universitario.html'
    form_class = EstudioUniversitarioForm
    success_url = reverse_lazy('proyeccionsocial:consulta_estudio_universitario')

class eliminarEstudioUniversitario(DeleteView):
    model = EstudioUniversitario
    template_name = 'app1/eliminar_estudio_universitario.html'
    success_url = reverse_lazy('proyeccionsocial:consulta_estudio_universitario')


#-----------------------------------------------------------------------------------------------


def consultaSolicitudServicioSocial(request):
    solicitudes_list=Solicitud.objects.order_by('carnet_estudiante')
    context = {
        'solicitudes_list': solicitudes_list,
    }
    return render(
        request,
        'app1/Solicitud.html', context
    )

class crearSolicitudServicioSocial(CreateView):
    template_name = 'app1/crear_solicitud_servicio_social.html'
    form_class = SolicitudForm
    success_url = reverse_lazy('proyeccionsocial:consulta_solicitud_servicio_social')

class editarSolicitudServicioSocial(UpdateView):
    model = Solicitud
    template_name = 'app1/crear_solicitud_servicio_social.html'
    form_class = SolicitudForm
    success_url = reverse_lazy('proyeccionsocial:consulta_solicitud_servicio_social')

class eliminarSolicitudServicioSocial(DeleteView):
    model = Solicitud
    template_name = 'app1/eliminar_estudio_universitario.html'
    success_url = reverse_lazy('proyeccionsocial:consulta_solicitud_servicio_social')


#-----------------------------------------------------------------------------------------------


class generarF1(ListView):
    model = Estudiante
    template_name = 'app1/Estudiante.html'
    context_object_name = 'estudiante'
    success_url = reverse_lazy('proyeccionsocial:generar_F1')  
     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = 'static/img/logoUPSAgro.png'
        archivo_imagen2 = 'static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 730, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 720, 125, 90,preserveAspectRatio=True) 

        # Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        # Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        # el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 780, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 770, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 760, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 750, u"UNIDAD DE PROYECCION SOCIAL")       

    def get_queryset(self, pdf, **kwargs):
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        queryset = Estudiante.objects.filter(carnet_estudiante = carnet_estudiante)

        for i in Estudiante.objects.filter(carnet_estudiante = carnet_estudiante):
            carnet = i.carnet_estudiante
            nombre = i.nombre_estudiante
            apellido = i.apellido_estudiante
            sexo = i.sexo_estudiante
            telefono = i.telefono_estudiante
            correo = i.correo_estudiante
            direccion = i.direccion_estudiante

        j=0

        for i in Estudiante.objects.all():
            carnetBusqueda = i.carnet_estudiante
            if carnetBusqueda == carnet:
                posicion = j + 1
            else:
                j = j + 1

        numero = posicion

        for i in EstudioUniversitario.objects.filter(carnet_estudiante = carnet_estudiante):
            carrera = i.codigo_carrera.nombre_carrera
            porc_carrera = i.porc_carrerar_aprob
            und_valor = i.unidades_valorativas
            experiencia = i.experiencia_areas_conoc
            ciclo_lect = i.codigo_ciclo

        for i in Solicitud.objects.filter(carnet_estudiante = carnet_estudiante):
            horas_sem = i.horas_semana
            dias_sem = i.dias_semana
            entidad = i.codigo_entidad
            modalidad = i.modalidad
            fecha_inicio = i.fecha_inicio
        
        aceptado = "NO"
        motivo = "Debe escoger otra entidad."
        observaciones = "Porfavor escoja otra entidad para poder realizar su servicio social."

        texto = 'No. Correlativo: %s' % numero
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(450, 705, texto)

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 720, u"F-1")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(235, 710, u"SOLICITUD DE SERVICIO SOCIAL")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 690, u"DATOS PERSONALES")

        texto = 'Nombre Completo: %s' % nombre +' '+ apellido
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 675, texto)

        #--------------------------------------
        #texto = 'Nombre Completo: ' 
        #pdf.setFont("Helvetica-Bold", 10)
        #pdf.drawString(60, 675, texto)

        #texto = ' %s' % nombre
        #pdf.setFont("Helvetica", 10)
        #pdf.drawString(150, 675, texto)
        #---------------------------------------

        texto = 'Sexo: %s' % sexo
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 660, texto)

        texto = 'Telefono: %s' % telefono
        pdf.setFont("Helvetica", 10)
        pdf.drawString(150, 660, texto)

        texto = 'Correo: %s' % correo
        pdf.setFont("Helvetica", 10)
        pdf.drawString(330, 660, texto)

        texto = 'Direccion Residencial: %s' % direccion
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 645, texto)

        #Agrega una linea horizontal como division
        pdf.line(60, 630, 560, 630)

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 610, u"ESTUDIO UNIVERSITARIO")

        texto = 'Carrera: %s' % carrera
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 595, texto)

        texto = 'Carnet No.: %s' % carnet
        pdf.setFont("Helvetica", 10)
        pdf.drawString(450, 595, texto)

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 575, u"Estado Academico:")

        texto = 'Porcentaje de la carrera aprobado: %s' % porc_carrera
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 560, texto)

        texto = 'Unidades Valorativas: %s' % und_valor
        pdf.setFont("Helvetica", 10)
        pdf.drawString(280, 560, texto)

        texto = 'Ciclo Lectivo: %s' % ciclo_lect
        pdf.setFont("Helvetica", 10)
        pdf.drawString(450, 560, texto)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 545, u"Experiencia en algunas areas de conocimiento de su carrera: ")

        texto = '%s' % experiencia
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 530, texto)

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 495, u"Tiempo disponible para su desarrollo social: ")

        texto = 'Horas por Semana: %s' % horas_sem
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 480, texto)

        texto = 'Dias por Semana: %s' % dias_sem
        pdf.setFont("Helvetica", 10)
        pdf.drawString(330, 480, texto)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 465, u"Propuesta de la entidad donde realizara su servicio social segun el ambito mencionado en el Manual de ")
        pdf.drawString(60, 450, u"procedimientos del Servicio Social: ")

        texto = '%s' % entidad
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 435, texto)

        #Agrega una linea horizontal como division
        pdf.line(60, 420, 560, 420)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 400, u"Propuesta de modalidad de servicio segun las mencionadas en el Manual de Procedimientos del Servicio ")

        texto = 'Social: %s' % modalidad
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 385, texto)

        texto = 'Fecha de Inicio posible: %s' % fecha_inicio
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 370, texto)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 335, u"Firma del solicitante: ")
        pdf.line(155, 335, 300, 335)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 305, u"Ciudad Universitaria, ")
        pdf.line(155, 305, 200, 305)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(210, 305, u"de")
        pdf.line(230, 305, 320, 305)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(330, 305, u"del ")
        pdf.line(350, 305, 410, 305)

        #Agrega una linea horizontal como division
        pdf.line(60, 285, 560, 285)

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 265, u"PARA USO EXCLUSIVO DE PROYECCION SOCIAL ")

        texto = 'Aceptado: %s' % aceptado
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 245, texto)

        texto = 'Motivo: %s' % motivo
        pdf.setFont("Helvetica", 10)
        pdf.drawString(200, 245, texto)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 225, u"Observaciones: ")

        texto = '%s' % observaciones
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 210, texto)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(generarF1, self).get_context_data(**kwargs)
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        context['carnet_estudiante'] = carnet_estudiante
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "Comprobante_F1_UPS.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


# #-----------------------------------------------------------------------------------------------


class generarF8(ListView):
    model = Estudiante
    template_name = 'app1/Estudiante.html'
    context_object_name = 'estudiante'
    success_url = reverse_lazy('proyeccionsocial:generar_F1')  
     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = 'static/img/logoUPSAgro.png'
        archivo_imagen2 = 'static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 730, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 720, 125, 90,preserveAspectRatio=True) 

        #Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        #Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        #el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 780, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 770, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 760, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 750, u"UNIDAD DE PROYECCION SOCIAL")        

    def get_queryset(self, pdf, **kwargs):
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        queryset = Estudiante.objects.filter(carnet_estudiante = carnet_estudiante)

        for i in Estudiante.objects.filter(carnet_estudiante = carnet_estudiante):
            carnet = i.carnet_estudiante
            nombre = i.nombre_estudiante
            apellido = i.apellido_estudiante

        for i in EstudioUniversitario.objects.filter(carnet_estudiante = carnet_estudiante):
            carrera = i.codigo_carrera.nombre_carrera

        for i in Solicitud.objects.filter(carnet_estudiante = carnet_estudiante):
            fecha_fin = i.fecha_fin
            fecha_inicio = i.fecha_inicio
        
        docenteTutor = "Marcia Lizeth Rivera García"

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 720, u"F-8")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 690, u"HOJA DE REGISTRO DE LAS HORAS SOCIALES REALIZADAS EN LA ESTACIÓN EXPERIMENTAL Y DE")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(180, 675, u"PRÁCTICAS POR ESTUDIANTES DE LA UNIVERSIDAD")

        texto = 'Nombre Completo:   %s' % nombre +' '+ apellido
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 630, texto)

        texto = 'Carnet No.:    %s' % carnet
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 610, texto)

        texto = 'Carrera:   %s' % carrera
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 590, texto)

        texto = 'Docente Tutor:   %s' % docenteTutor
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 570, texto)

        cx=60
        cy=515
        ancho=55
        alto=40
        pdf.rect(cx, cy, ancho, alto)

        texto = 'FECHA'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(70, 530, texto)

        cx=115
        cy=515
        ancho=57
        alto=40
        pdf.rect(cx, cy, ancho, alto)

        texto = 'HORA DE'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(121, 535, texto)

        texto = 'ENTRADA'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(120, 525, texto)

        cx=172
        cy=515
        ancho=250
        alto=40
        pdf.rect(cx, cy, ancho, alto)

        texto = 'ACTIVIDAD REALIZADA'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(235, 530, texto)

        cx=422
        cy=515
        ancho=57
        alto=40
        pdf.rect(cx, cy, ancho, alto)

        texto = 'HORA DE'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(428, 535, texto)

        texto = 'SALIDA'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(432, 525, texto)

        cx=479
        cy=515
        ancho=70
        alto=40
        pdf.rect(cx, cy, ancho, alto)

        texto = 'HORAS'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(495, 535, texto)

        texto = 'REALIZADAS'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(483, 525, texto)

#-------------- FILA 1 ------------------------------        

        cx=60
        cy=490
        ancho=55
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=115
        cy=490
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=172
        cy=490
        ancho=250
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=422
        cy=490
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=479
        cy=490
        ancho=70
        alto=25
        pdf.rect(cx, cy, ancho, alto)

#-------------- FILA 2 ------------------------------   

        cx=60
        cy=465
        ancho=55
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=115
        cy=465
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=172
        cy=465
        ancho=250
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=422
        cy=465
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=479
        cy=465
        ancho=70
        alto=25
        pdf.rect(cx, cy, ancho, alto)

#-------------- FILA 3 ------------------------------   

        cx=60
        cy=440
        ancho=55
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=115
        cy=440
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=172
        cy=440
        ancho=250
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=422
        cy=440
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=479
        cy=440
        ancho=70
        alto=25
        pdf.rect(cx, cy, ancho, alto)

#-------------- FILA 4 ------------------------------   

        cx=60
        cy=415
        ancho=55
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=115
        cy=415
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=172
        cy=415
        ancho=250
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=422
        cy=415
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=479
        cy=415
        ancho=70
        alto=25
        pdf.rect(cx, cy, ancho, alto)

#-------------- FILA 5 ------------------------------   

        cx=60
        cy=390
        ancho=55
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=115
        cy=390
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=172
        cy=390
        ancho=250
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=422
        cy=390
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=479
        cy=390
        ancho=70
        alto=25
        pdf.rect(cx, cy, ancho, alto)

#-------------- FILA 6 ------------------------------   

        cx=60
        cy=365
        ancho=55
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=115
        cy=365
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=172
        cy=365
        ancho=250
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=422
        cy=365
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=479
        cy=365
        ancho=70
        alto=25
        pdf.rect(cx, cy, ancho, alto)

#---------------------------------------------------------------- 

        texto = 'Este registro de actividades comprende del día:    %s' %fecha_inicio
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 330, texto)

        texto = ';Al día:   %s' %fecha_fin
        pdf.setFont("Helvetica", 10)
        pdf.drawString(340, 330, texto)

    # ----------- FIRMAS ----------------#

        x1 = 100
        y1 = 280
        x2 = 500
        y2 = 280
        pdf.line(x1, y1, x2, y2)

        texto = 'NOMBRE Y FIRMA DEL COORDINADOR DE LA EXTENSION AGROPECUARIA DE LA EEP'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(90, 260, texto)

        x1 = 100
        y1 = 200
        x2 = 500
        y2 = 200
        pdf.line(x1, y1, x2, y2)

        texto = 'Vo. Bo. DIRECTOR DE LA ESTACIÓN EXPERIMENTAL Y DE PRÁCTICAS'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(130, 180, texto) 

        texto = 'SELLO'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(285, 130, texto) 

        x1 = 180
        y1 = 90
        x2 = 430
        y2 = 90
        pdf.line(x1, y1, x2, y2)

        texto = 'NOMBRE Y FIRMA DEL DOCENTE TUTOR'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(200, 70, texto)

    # ----------------------------------------- #

        return queryset

    def get_context_data(self, **kwargs):
        context = super(generarF1, self).get_context_data(**kwargs)
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        context['carnet_estudiante'] = carnet_estudiante
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "Comprobante_F8_UPS.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


# #-----------------------------------------------------------------------------------------------


class generarF7(ListView):
    model = Estudiante
    template_name = 'app1/Estudiante.html'
    context_object_name = 'estudiante'
    success_url = reverse_lazy('proyeccionsocial:generar_F7')  
     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = 'static/img/logoUPSAgro.png'
        archivo_imagen2 = 'static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 730, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 720, 125, 90,preserveAspectRatio=True) 

        # Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        # Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        # el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 780, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 770, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 760, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 750, u"UNIDAD DE PROYECCION SOCIAL")         

    def get_queryset(self, pdf, **kwargs):
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        queryset = Estudiante.objects.filter(carnet_estudiante = carnet_estudiante)
        #Declaracion y asignacion de variables que se recuperaran de la BD
        nomproy= "Manejo de Base de Datos"
        nombre = "Robeto Carlos, Paz Ramirez"
        numExpediente= "12"
        departamento= "Inteligencia Informatica"
        entidad = "Facultad de Ingeneria y Arquitectura, UES"
        lugarPrestServ= "San Salvador"
        numInforme= 32
        fecha_inicio = "12/10/20"
        fecha_fin="12/10/21"
        horasrepActual="450"
        horasTot="500"
        sexo = "M"
        telefono = "7452-2749"
        correo = "rm17039@ues.edu.sv"
        direccion = "8va. Calle Poniente Barrio San Sebastian Analco Casa No. 38 A, Zacatecoluca, La Paz."
        carrera = "Ingenieria de Sistemas Informaicos"
        carnet = "RM17039"
        porc_carrera = 60
        und_valor = 100
        ciclo_lect = "Impar"
        experiencia = "Desarrollo y conocimiento en html, java, javascript, python, php, css etc. "
        horas_sem = 24
        dias_sem = 6
        modalidad = "Presencial"

        aceptado = "SI"
        motivo = "Faltan Datos"
        observaciones = "Buscar otra institucion y presentarla lo mas antes posible a la secretaria de proyeccion social"

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 720, u"F-7")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(200, 710, u"FORMATO DEL INFORME DE SERVIVIO SOCIAL")

        cx=55
        cy=685
        ancho=500
        alto=20
        pdf.rect(cx, cy, ancho, alto)

        texto = 'NOMBRE DEL PROYECTO: %s' % nomproy
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 690, texto)

        cx=55
        cy=570
        ancho=500
        alto=100
        pdf.rect(cx, cy, ancho, alto)            

        texto = 'NOMBRE DEL ALUMNO: %s' % nombre
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 655, texto)

        texto = 'NÚMERO DE CARNÉ: %s' % carnet
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 635, texto)

        texto = 'No. EXPEDIENTE: %s' % numExpediente
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 615, texto)

        texto = 'DEPARTAMENTO: %s' % departamento
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 595, texto)

        texto = 'CARRERA: %s' % carrera
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 575, texto)       

        cx=55
        cy=515
        ancho=500
        alto=40
        pdf.rect(cx, cy, ancho, alto)            

        texto = 'ENTIDAD DONDE REALIZA EL SERVICIO: %s' % entidad
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 540, texto)                  

        texto = 'LUGAR DE PRESTACIÓN DEL SERVICIO SOCIAL: %s' % lugarPrestServ 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 520, texto)   
        

        texto = 'NUMERO DE INFORME: %s' % numInforme 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 485, texto) 

        cx=55
        cy=440
        ancho=500
        alto=60
        pdf.rect(cx, cy, ancho, alto)                   

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 465, u'PERIODO REPORTADO: ')  

        texto = 'Del día:   %s' % fecha_inicio
        pdf.setFont("Helvetica", 10)
        pdf.drawString(180, 465, texto)      

        texto = ';al día:   %s' % fecha_fin
        pdf.setFont("Helvetica", 10)
        pdf.drawString(280, 465, texto)           

        texto = 'Total de horas de este reporte: %s' % horasrepActual
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 445, texto)                           

        texto = 'Total de horas Acumuladas: %s' % horasTot
        pdf.setFont("Helvetica", 10)
        pdf.drawString(250, 445, texto)  

        cx=55
        cy=355
        ancho=500
        alto=70
        pdf.rect(cx, cy, ancho, alto)   

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 410, u'DESCRIPCIÓN DE ACTIVIDADES: Máximo 2 páginas en tamaño carta ')  

        texto = 'Se describira tofo lo que se haya dearrollado en las 250 horas dentro del proyecto de servicio social y de '
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 390, texto)  

        texto = 'acuerdo con lo programado en el cronograma de actividades. A si mismo, se indicara el cumplimiento o '
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 380, texto)  

        texto = 'incumplimeinto de dichas actividades indicando las razones. Tambien podran ser añadidas observaciones '
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 370, texto)       

        #########FIRMAS############

        x1 = 80
        y1 = 300
        x2= 280
        y2= 300
        pdf.line(x1, y1, x2, y2)

        texto = 'NOMBRE Y FIRMA TUTOR INTERNO'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(90, 290, texto)
        pdf.drawString(160, 270, u'SELLO') 

        x1 = 330
        y1 = 300
        x2 = 530
        y2= 300
        pdf.line(x1, y1, x2, y2)

        texto = 'NOMBRE Y FIRMA TUTOR EXTERNO'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(340, 290, texto) 
        pdf.drawString(410, 270, u'SELLO') 

        x1 = 205
        y1 = 230
        x2 = 405
        y2= 230
        pdf.line(x1, y1, x2, y2)

        texto = 'FIRMA DEL ESTUDIANTE'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(245, 220, texto) 

        x1 = 205
        y1 = 160
        x2 = 405
        y2= 160
        pdf.line(x1, y1, x2, y2)

        texto = 'Vo. Bo. COORDINADOR DE PROYECCIÓN SOCIAL DEL DEPARTAMENTO'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(135, 150, texto) 
        ##############################

        texto = 'NOTA: ESTE INFORME DEBERÁ SER PRESENTADO EN DIGITAL Y EN FISICO, CADA 250 HORAS,'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(80, 120, texto)  

        texto = 'DENTRO DE LOS PRIMEROS 5 DÍAS HÁBILES DE LA FECHA DE TÉRMINO DEL MISMO, DE LO '
        pdf.setFont("Helvetica", 10)
        pdf.drawString(80, 110, texto)  

        texto = 'CONTRARIO PROCEDERÁ SANCIÓN DE ACUERDO AL REGLAMENTO VIGENTE'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(80, 100, texto) 

        return queryset

    def get_context_data(self, **kwargs):
        context = super(generarF7, self).get_context_data(**kwargs)
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        context['carnet_estudiante'] = carnet_estudiante
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "Comprobante_F7_UPS.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


# #------------------------------------------------------------------------------------------------------------------


class generarF9(ListView):
    model = Estudiante
    template_name = 'app1/Estudiante.html'
    context_object_name = 'estudiante'
    success_url = reverse_lazy('proyeccionsocial:generar_F9')  
     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = 'static/img/logoUPSAgro.png'
        archivo_imagen2 = 'static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 730, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 720, 125, 90,preserveAspectRatio=True) 

        # Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        # Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        # el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 780, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 770, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 760, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 750, u"UNIDAD DE PROYECCION SOCIAL")     

    def get_queryset(self, pdf, **kwargs):
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        queryset = Estudiante.objects.filter(carnet_estudiante = carnet_estudiante)
        #Declaracion y asignacion de variables que se recuperaran de la BD
        numero = 1
        nombre = "Noel Alexander Renderos Martinez"
        sexo = "M"
        telefono = "7452-2749"
        correo = "rm17039@ues.edu.sv"
        direccion = "8va. Calle Poniente Barrio San Sebastian Analco Casa No. 38 A, Zacatecoluca, La Paz."
        carrera = "Ingenieria de Sistemas Informaicos"
        carnet = "RM17039"
        porc_carrera = 60
        und_valor = 100
        ciclo_lect = "Impar"
        experiencia = "Desarrollo y conocimiento en html, java, javascript, python, php, css etc. "
        horas_sem = 24
        dias_sem = 6
        entidad = "Facultad de Ingeneria y Arquitectura, UES"
        modalidad = "Presencial"
        fecha_inicio = "12/10/20"
        fecha_fin= "12/10/21"
        aceptado = "SI"
        motivo = "Faltan Datos"
        observaciones = "Buscar otra institucion y presentarla lo mas antes posible a la secretaria de proyeccion social"

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 715, u"F-9")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(90, 660, u"CONSTANCIA HORAS SOCIALES EN LA ESTACIÓN EXPERIMENTAL Y DE PRÁCTICAS")

        texto = 'El suscrito, coordinador de Extensión Agropecuaria de la Estación Experimental y de Prácticas, ' 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 620, texto)

        texto = 'hace constar que el(la)' 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 600, texto)

        texto = 'Bachiller:   %s' % nombre
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 580, texto)   

        texto = 'Carné No.: %s' % carnet
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 560, texto)    

        texto = 'matriculado(a) en la carrera:'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(200, 560, texto)        

        texto = '%s' % carrera
        pdf.setFont("Helvetica", 10)
        pdf.drawString(180, 540, texto)  

        x1 = 60
        y1 = 525
        x2 = 530
        y2 = 525
        pdf.line(x1, y1, x2, y2)    

        texto = 'ha cumplido satisfactoriamnet las horas sociales correspondientes al 25% de su servicio social en'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 500, texto)   

        texto = 'esta unidad, conforme al plan de trabajo diseñado para el perido:'
        pdf.drawString(60, 480, texto)   

        texto = 'Del día: %s' % fecha_inicio
        pdf.setFont("Helvetica", 10)
        pdf.drawString(180, 460, texto)      

        texto = ';al día: %s' % fecha_fin
        pdf.setFont("Helvetica", 10)
        pdf.drawString(260, 440, texto) 

        x1 = 60
        y1 = 150
        x2 = 520
        y2 = y1
        pdf.line(x1, y1, x2, y2)

        texto = 'NOMBRE Y FIRMA DEL DOCENTE TUTOR'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(200, 140, texto) 

        x1 = 60
        y1 = 250
        x2 = 520
        y2 = y1
        pdf.line(x1, y1, x2, y2)

        texto = 'Vo. Bo. DIRECTOR DE LA ESTACIÓN EXPERIMENTAL Y DE PRÁCTICAS'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(130, 240, texto)
        pdf.drawString(270, 220, u'SELLO')         

        x1 = 60
        y1 = 350
        x2 = 520
        y2 = y1
        pdf.line(x1, y1, x2, y2)

        texto = 'NOMBRE Y FIRMA DEL COORDINADOR DE EXTENSION AGROPECUARIA'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(130, 330, texto)

        return queryset
 
    def get_context_data(self, **kwargs):
        context = super(generarF9, self).get_context_data(**kwargs)
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        context['carnet_estudiante'] = carnet_estudiante
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "Comprobante_F9_UPS.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response