from django import forms

from django.forms import widgets
#from datetime import datetime
#import time
#from datetime import date

from gestionStock.models import Medicamentos, Lotes, Farmacias





# =======================================================================
# Formulario Nuevo Stock =================================================
# =======================================================================
class Formulario_nuevo_stock(forms.ModelForm):

        #principio_activo = forms.CharField()
        # aca se enumeran los campos que se van a mostrar con el formulario
        class Meta:
                model = Lotes
                fields = ['medicamento','stock','vencimiento']

        # intento hacer la verificacion de la fechas 
        
        #def clean_vencimiento(self):
        #        today = date.today()
        #        vencimiento = self.cleaned_data['vencimiento']
        #        if vencimiento < str(today):
        #                print("la fecha esta vencida")
        #                raise forms.ValidationError("La fecha de vencimiento no puede ser anterior a hoy!")
        #        if vencimiento > str(today):
        #                print("la fecha NO esta vencida")
        #                #raise forms.ValidationError("La fecha de vencimiento no puede ser anterior a hoy!")
        #        return vencimiento


        #===============================================
        # aca se definen las clases de bootstrap que se le 
        # aplican a los campos del formulario _nuevo_stock 
        #===============================================
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['medicamento'].widget.attrs.update({'class': 'form-control'})
                self.fields['stock'].widget.attrs.update({'class': 'form-control'})
                self.fields['stock'].widget.attrs.update(value='100')
                #self.fields['ubicacion'].widget.attrs.update({'class': 'form-control'})
                self.fields['vencimiento'].widget.attrs.update({'class': 'form-control','required':'required'})


# =======================================================================
# Nuevo Stock para el funcionarios auditor de stock=================================================
# =======================================================================
class Formulario_nuevo_stock_con_farmacias(forms.ModelForm):

        #principio_activo = forms.CharField()
        # aca se enumeran los campos que se van a mostrar con el formulario
        class Meta:
                model = Lotes
                fields = ['medicamento','stock', 'ubicacion','vencimiento']


        #===============================================
        # aca se definen las clases de bootstrap que se le 
        # aplican a los campos del formulario _nuevo_stock 
        #===============================================
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['medicamento'].widget.attrs.update({'class': 'form-control'})
                self.fields['stock'].widget.attrs.update({'class': 'form-control'})
                self.fields['stock'].widget.attrs.update(value='100')
                self.fields['ubicacion'].widget.attrs.update({'class': 'form-control'})
                self.fields['vencimiento'].widget.attrs.update({'class': 'form-control','required':'required'})





# =======================================================================
# Formulario Nuevo Medicamento ============================================
# =======================================================================
class Formulario_nuevo_medicamento(forms.Form):

        # aca se enumeran los campos que se van a mostrar con el formulario
        class Meta:
                model = Medicamentos
                fields = ['nombre_comercial','categoria','laboratorio','principio_activo','forma','contraindicaciones']



class Formulario_nueva_farmacia(forms.ModelForm):

        #principio_activo = forms.CharField()
        # aca se enumeran los campos que se van a mostrar con el formulario
        class Meta:
                model = Farmacias
                fields = ['nombre','direccion','localidad','departamento','funcionarios']


        #===============================================
        # aca se definen las clases de bootstrap que se le 
        # aplican a los campos del formulario _nuevo_stock 
        #===============================================
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
                self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
                self.fields['localidad'].widget.attrs.update({'class': 'form-control'})
                self.fields['departamento'].widget.attrs.update({'class': 'form-control'})
                self.fields['funcionarios'].widget.attrs.update({'class': 'form-control'})
