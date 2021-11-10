from django import forms
from django.forms import widgets

from gestionUsuarios.models import Usuarios
#from django.contrib.
#from allauth.account.forms import ResetPasswordForm


#class ResetPasswordForm(PasswordResetForm):
#class PasswordResetForm(ResetPasswordForm):
class PasswordResetForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = ""
        self.fields['email'].widget = forms.EmailInput(attrs={"placeholder": "Direccion de E-maill"})