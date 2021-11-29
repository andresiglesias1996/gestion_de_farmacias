from django import forms

from django.forms import widgets

from gestionStock.models import Medicamentos, Lotes





# =======================================================================
# Formulario Nuevo Stock =================================================
# =======================================================================
class Formulario_nuevo_stock(forms.ModelForm):

        #principio_activo = forms.CharField()
        # aca se enumeran los campos que se van a mostrar con el formulario
        class Meta:
                model = Lotes
                fields = ['medicamento','stock','vencimiento']


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



