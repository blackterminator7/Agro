from django import forms
from .models import *
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.postgres.fields import ArrayField

sexo = [('M', 'M'), ('F', 'F'), ]
estado = [('Aceptado', 'Aceptado'), ('Denegado', 'Denegado')]


class CicloForm(forms.ModelForm):
    class Meta:
        model = Ciclo
        widgets = {
            'codigo_ciclo': forms.TextInput(attrs={'placeholder': 'Código Ciclo', 'autofocus': '', 'required': '', 'maxlength':'5'}),
            'tipo_ciclo': forms.TextInput(attrs={'placeholder': 'Ciclo Lectivo', 'autofocus': '', 'required': ''}),
        }
        fields = {
            'codigo_ciclo': forms.IntegerField,
            'tipo_ciclo': forms.CharField,
        }
        labels = {
            'codigo_ciclo': 'Codigo Ciclo',
            'tipo_ciclo': 'Ciclo Lectivo',
        }

    def __init__(self, *args, **kwargs):
        super(CicloForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
                })



class  EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        widgets = {
            'carnet_estudiante': forms.TextInput(attrs={'placeholder': 'Carnet Estudiante', 'autofocus': '', 'required': ''}),
            'nombre_estudiante': forms.TextInput(attrs={'placeholder': 'Nombres Estudiante', 'autofocus': '', 'required': ''}),
            'apellido_estudiante': forms.TextInput(attrs={'placeholder': 'Apellidos Estudiante', 'autofocus': '', 'required': ''}),
            'sexo_estudiante': forms.Select(choices=sexo),
            'telefono_estudiante': forms.TextInput(attrs={'placeholder': 'Telefono Estudiante', 'autofocus': '', 'required': '', 'maxlength':'8'}),
            'correo_estudiante': forms.TextInput(attrs={'placeholder': 'Correo Estudiante', 'autofocus': '', 'required': ''}),
            'direccion_estudiante': forms.TextInput(attrs={'placeholder': 'Direccion Estudiante', 'autofocus': '', 'required': ''}),
        }
        fields = {
            'carnet_estudiante': forms.CharField,
            'nombre_estudiante': forms.CharField,
            'apellido_estudiante': forms.CharField,
            'sexo_estudiante': forms.CharField,
            'telefono_estudiante': forms.IntegerField,
            'correo_estudiante': forms.CharField,
            'direccion_estudiante': forms.CharField,
        }
        labels = {
            'carnet_estudiante': 'Carnet',
            'nombre_estudiante':'Nombre',
            'sexo_estudiante': 'Sexo',
            'telefono_estudiante': 'Telefono',
            'correo_estudiante': 'Correo',
            'direccion_estudiante': 'Direccion',
        }

    def __init__(self, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
                })



class EstudioUniversitarioForm(forms.ModelForm):
    codigo_carrera = forms.ModelChoiceField(queryset=Carrera.objects.all().order_by('nombre_carrera'))
    codigo_ciclo = forms.ModelChoiceField(queryset=Ciclo.objects.all().order_by('codigo_ciclo'))
    carnet_estudiante = forms.ModelChoiceField(queryset=Estudiante.objects.all().order_by('carnet_estudiante'))

    class Meta:
        model = EstudioUniversitario
        widgets = {
            'porc_carrerar_aprob': forms.TextInput(attrs={'placeholder': 'Porcentaje Carrera Aprobado', 'autofocus': '', 'required': '', 'maxlength':'3'}),
            'unidades_valorativas': forms.TextInput(attrs={'placeholder': 'Unidades Valorativas', 'autofocus': '', 'required': '',  'maxlength':'3'}),
            'experiencia_areas_conoc': forms.TextInput(attrs={'placeholder': 'Experiencia en Areas Conocidas', 'autofocus': '', 'required': ''}),
        }
        fields = {
            'carnet_estudiante': forms.CharField,
            'codigo_carrera': forms.CharField,
            'codigo_ciclo': forms.IntegerField,
            'porc_carrerar_aprob': forms.IntegerField,
            'unidades_valorativas': forms.IntegerField,
            'experiencia_areas_conoc': forms.CharField,
        }
        labels = {
            'carnet_estudiante': 'Carnet Estudiante',
            'codigo_carrera': 'Carrera Estudiante',
            'codigo_ciclo': 'Ciclo',
            'porc_carrerar_aprob': 'Porcentaje Carrera Aprobado',
            'unidades_valorativas': 'Unidades Valorativas',
            'experiencia_areas_conoc': 'Experiencia en Areas Conocidas',
        }

    def __init__(self, *args, **kwargs):
        super(EstudioUniversitarioForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
                })

    def clean(self, *args, **kwargs):
        cleaned_data = super(EstudioUniversitarioForm, self).clean(*args, **kwargs)
        porc_carrerar_aprob = cleaned_data.get('porc_carrerar_aprob', None)
        if porc_carrerar_aprob is not None:
            if porc_carrerar_aprob < 60:
                self.add_error('porc_carrerar_aprob', 'Aun no esta apto para realizar el servicio social.')


class SolicitudForm(forms.ModelForm):
    codigo_entidad = forms.ModelChoiceField(queryset=EntidadExterna.objects.all().order_by('nombre_entidad'))
    carnet_estudiante = forms.ModelChoiceField(queryset=Estudiante.objects.all().order_by('carnet_estudiante'))

    class Meta:
        model = Solicitud
        widgets = {
            'horas_semana': forms.TextInput(attrs={'placeholder': 'Horas a la Semana', 'autofocus': '', 'required': '', 'maxlength':'3'}),
            'dias_semana': forms.TextInput(attrs={'placeholder': 'Días a la Semana', 'autofocus': '', 'required': '',  'maxlength':'1'}),
            'modalidad': forms.TextInput(attrs={'placeholder': 'Modalidad del Servicio', 'autofocus': '', 'required': ''}),
            'fecha_inicio': forms.TextInput(attrs={'placeholder': 'Fecha de Inicio', 'autocomplete': 'off', 'type':'date', 'min':'1940-01-01'}),
            'fecha_fin': forms.TextInput(attrs={'placeholder': 'Fecha de Finalización', 'autocomplete': 'off', 'type':'date', 'min':'1940-01-01', 'required':'false'}),
        }
        fields = {
            'carnet_estudiante': forms.CharField,
            'codigo_entidad': forms.CharField,
            'horas_semana': forms.CharField,
            'dias_semana': forms.CharField,
            'modalidad': forms.IntegerField,
            'fecha_inicio': forms.DateField,
            'fecha_fin': forms.DateField,
        }
        labels = {
            'carnet_estudiante': 'Carnet Estudiante',
            'codigo_entidad': 'Nombre de la Entidad',
            'horas_semana': 'Horas a la Semana',
            'dias_semana': 'Días a la Semana',
            'modalidad': 'Modalidad del Servicio',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha Finalización',
        }

    def __init__(self, *args, **kwargs):
        super(SolicitudForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
                })