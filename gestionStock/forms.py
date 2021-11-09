from django import forms

from django.forms import widgets

from gestionStock.models import Medicamentos, Lotes





# =======================================================================
# Crear Stock ============================================================
# =======================================================================
class Formulario_nuevo_stock(forms.ModelForm):

        class Meta:
                model = Lotes
                fields = ['medicamento','stock','ubicacion','vencimiento']


        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['medicamento'].widget.attrs.update({'class': 'form-control'})
                self.fields['stock'].widget.attrs.update({'class': 'form-control'})
                self.fields['stock'].widget.attrs.update(value='100')
                self.fields['ubicacion'].widget.attrs.update({'class': 'form-control'})
                self.fields['vencimiento'].widget.attrs.update({'class': 'form-control','required':'required'})






# =======================================================================
# Crear Medicamento ======================================================
# =======================================================================
class Formulario_nuevo_medicamento(forms.Form):

        class Meta:
                model = Medicamentos
                fields = ['nombre_comercial','categoria','laboratorio','principio_activo','forma','contraindicaciones']



