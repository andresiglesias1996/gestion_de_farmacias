from django import forms
from django.forms import widgets

from gestionUsuarios.models import Usuarios, Recetas




# =======================================================================
# Crear Usuario ==========================================================
# =======================================================================
class FormularioCrearUsuario(forms.ModelForm):
        #formulario de registro de un Usuario en la base de datos
        
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['cedula_de_identidad'].widget.attrs.update({'class': 'form-control'})
                #self.fields['rol'].widget.attrs.update({'class': 'form-control'})
                self.fields['usuario'].widget.attrs.update({'class': 'form-control'})
                self.fields['email'].widget.attrs.update({'class': 'form-control'})
                self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
                self.fields['apellido'].widget.attrs.update({'class': 'form-control'})
                self.fields['sexo'].widget.attrs.update({'class': 'form-control'})
                self.fields['fecha_de_nacimiento'].widget.attrs.update({'class': 'form-control'})
                self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
                self.fields['departmento'].widget.attrs.update({'class': 'form-control'})
                self.fields['telefono'].widget.attrs.update({'class': 'form-control'})



                #self.fields['comment'].widget.attrs.update(size='40')
       

        #password1 es la contraseña
        #password2 es la verificacion de la contraseña

        password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
                attrs={
                        'class':'form-control',
                        #'placeholder': 'Ingrese su contraseña...',
                        'id':'password1',
                        'required':'required'
                }
        ))
        
        password2 = forms.CharField(label='Confirmación de contraseña', widget=forms.PasswordInput(
                attrs={
                        'class':'form-control',
                        #'placeholder': 'Ingrese nuevamente su contraseña...',
                        'id':'password2',
                        'required':'required',
                }
        ))


        class Meta:
                model= Usuarios
                fields = ['cedula_de_identidad','usuario','email','nombre','apellido','sexo','fecha_de_nacimiento','direccion','departmento','telefono']
                
                


        def clean_password2(self):
                #validacion de contraseñas

                password1 = self.cleaned_data.get("password1")
                password2 = self.cleaned_data.get("password2")
                if password1 and password2 and password1 != password2:
                        raise forms.ValidationError("Las contraseñas no coinciden.")
                return password2

        def save(self, commit = True):
                user = super().save(commit = False)
                user.set_password(self.cleaned_data.get('password1'))
                if commit:
                        user.save()
                return user




# =======================================================================
# Editar Usuario =========================================================
# =======================================================================
class FormularioEditarUsuario(forms.ModelForm):
        #formulario de registro de un Usuario en la base de datos
        
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                #self.fields['cedula_de_identidad'].widget.attrs.update({'class': 'form-control'})
                self.fields['rol'].widget.attrs.update({'class': 'form-control'})
                self.fields['email'].widget.attrs.update({'class': 'form-control'})
                self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
                self.fields['apellido'].widget.attrs.update({'class': 'form-control'})
                self.fields['sexo'].widget.attrs.update({'class': 'form-control'})
                self.fields['fecha_de_nacimiento'].widget.attrs.update({'class': 'form-control'})
                self.fields['telefono'].widget.attrs.update({'class': 'form-control'})

                #self.fields['comment'].widget.attrs.update(size='40')
       

        #password1 es la contraseña
        #password2 es la verificacion de la contraseña

        password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
                attrs={
                        'class':'form-control',
                        #'placeholder': 'Ingrese su contraseña...',
                        'id':'password1',
                        'required':'required'
                }
        ))
        
        password2 = forms.CharField(label='Confirmación de contraseña', widget=forms.PasswordInput(
                attrs={
                        'class':'form-control',
                        #'placeholder': 'Ingrese nuevamente su contraseña...',
                        'id':'password2',
                        'required':'required',
                }
        ))


        class Meta:
                model= Usuarios
                fields = ['rol','email','nombre','apellido','sexo','fecha_de_nacimiento','telefono']
                
                


        def clean_password2(self):
                #validacion de contraseñas

                password1 = self.cleaned_data.get("password1")
                password2 = self.cleaned_data.get("password2")
                if password1 and password2 and password1 != password2:
                        raise forms.ValidationError("Las contraseñas no coinciden.")
                return password2

        def save(self, commit = True):
                user = super().save(commit = False)
                user.set_password(self.cleaned_data.get('password1'))
                if commit:
                        user.save()
                return user


# =======================================================================
# Formulario Editar Usuario 2 ===========================================================
# =======================================================================
# este formulario lo usamos en la pagina mi_usuario
# no permite editar c.i., usuario, passoword
class FormularioEditarUsuario_2(forms.ModelForm):

        class Meta:
                model = Usuarios
                fields = ['nombre','apellido','email','sexo','fecha_de_nacimiento','telefono']

        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
                self.fields['apellido'].widget.attrs.update({'class': 'form-control'})
                self.fields['email'].widget.attrs.update({'class': 'form-control'})
                self.fields['sexo'].widget.attrs.update({'class': 'form-control'})
                self.fields['fecha_de_nacimiento'].widget.attrs.update({'class': 'form-control','type':'date'})
                self.fields['telefono'].widget.attrs.update({'class': 'form-control'})




# =======================================================================
# Crear Receta ===========================================================
# =======================================================================
class Formulario_nueva_receta(forms.ModelForm):

        class Meta:
                model = Recetas
                #borramos el campo 'medico' porque se agrega automaticamente el usuario medico cuando se crea la receta
                fields = ['medicamento','paciente','descripcion','vencimiento','estado']

        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['medicamento'].widget.attrs.update({'class': 'form-control'})
                self.fields['paciente'].widget.attrs.update({'class': 'form-control'})
                #self.fields['medico'].widget.attrs.update({'class': 'form-control'})
                self.fields['descripcion'].widget.attrs.update({'class': 'form-control'})
                self.fields['vencimiento'].widget.attrs.update({'class': 'form-control','type':'date'})
                #self.fields['vencimiento'].widget.attrs.update(type='date')
                self.fields['estado'].widget.attrs.update({'class': 'form-control'})



class Formulario_receta_usuario(forms.ModelForm):



        class Meta:
                
                model= Usuarios
                model = Recetas
        
                fields = ['medicamento','paciente','medico','descripcion','vencimiento','estado']
              

        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['medicamento'].widget=forms.TextInput({'class': 'form-control'})
                self.fields['paciente'].widget=forms.TextInput({'class': 'form-control'})
                self.fields['medico'].widget=forms.TextInput({'class': 'form-control'})
                self.fields['descripcion'].widget=forms.TextInput({'class': 'form-control'})
                self.fields['vencimiento'].widget=forms.TextInput({'class': 'form-control','type':'date'})
                self.fields['estado'].widget=forms.TextInput({'class': 'form-control'}) 
                self.fields['usuario'].widget=forms.TextInput({'class': 'form-control'})
                self.fields['cedula_de_identidad'].widget=forms.TextInput({'class': 'form-control'})        