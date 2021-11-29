from django import forms
from django.forms import widgets

from gestionUsuarios.models import Usuarios, Recetas
from gestionStock.models import Medicamentos



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
                self.fields['departamento'].widget.attrs.update({'class': 'form-control'})
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
                fields = ['cedula_de_identidad','usuario','email','nombre','apellido','sexo','fecha_de_nacimiento','direccion','departamento','telefono']
                
                


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


def obtener_principios_activos():

        lista_de_principios_activos =(
                ("el 1", "One"),
                ("el 2", "Two"),
                ("el 3", "Three"),
                ("el 4", "Four"),
                ("el 5", "Five"),
        )

        lista_de_medicamentos = []
        queryset_de_medicamentos = Medicamentos.objects.all()
        print("==================medicamentos===================")
        print(queryset_de_medicamentos)

        if len(queryset_de_medicamentos) > 0:

                for medicamento in queryset_de_medicamentos:
                        mi_tupla = (medicamento.principio_activo,medicamento.principio_activo)
                        lista_de_medicamentos.append(mi_tupla)

        print("=========================")
        print(lista_de_medicamentos)
        #return lista_de_medicamentos

        return lista_de_principios_activos

# =======================================================================
# Crear Receta ===========================================================
# =======================================================================
class Formulario_nueva_receta(forms.ModelForm):

        principio_activo = forms.ChoiceField(choices=[])
        
        class Meta:
                model = Recetas
                
                #borramos el campo 'medico' porque se agrega automaticamente el usuario medico cuando se crea la receta
                fields = ['principio_activo','paciente','descripcion','vencimiento','cronico']


        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                
                #con esta linea genero la lista de tuplas que necesita el argumento choices del campo Principio activo
                # traigo todos los medicamentos y obtengo el campo principio_activo 
                principio_activo_choices_con_duplicados = [(medicamento.principio_activo, medicamento.principio_activo) for medicamento in Medicamentos.objects.all()]
                
                #el siguiente casting se hace para eliminar los valores duplicados
                #y la funcion sorted lo ordena alfabeticamente
                principio_activo_choices = sorted(list(dict.fromkeys(principio_activo_choices_con_duplicados)))
                #print("=================================")
                #print(principio_activo_choices)
                self.fields['principio_activo'].choices = principio_activo_choices
                
                self.fields['principio_activo'].widget.attrs.update({'class': 'form-control'})
                self.fields['paciente'].widget.attrs.update({'class': 'form-control'})
                #self.fields['medico'].widget.attrs.update({'class': 'form-control'})
                self.fields['descripcion'].widget.attrs.update({'class': 'form-control'})
                self.fields['vencimiento'].widget.attrs.update({'class': 'form-control','type':'date'})
                #self.fields['vencimiento'].widget.attrs.update(type='date')
                self.fields['cronico'].widget.attrs.update({'class': 'radio'})



class Formulario_receta_usuario(forms.ModelForm):



        class Meta:
                
                model= Usuarios
                model = Recetas
        
                fields = ['principio_activo','paciente','medico','descripcion','vencimiento','estado']
              

        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['principio_activo'].widget=forms.TextInput({'class': 'form-control'})
                self.fields['paciente'].widget=forms.TextInput({'class': 'form-control'})
                self.fields['medico'].widget=forms.TextInput({'class': 'form-control'})
                self.fields['descripcion'].widget=forms.TextInput({'class': 'form-control'})
                self.fields['vencimiento'].widget=forms.TextInput({'class': 'form-control','type':'date'})
                self.fields['estado'].widget=forms.TextInput({'class': 'form-control'}) 
                self.fields['usuario'].widget=forms.TextInput({'class': 'form-control'})
                self.fields['cedula_de_identidad'].widget=forms.TextInput({'class': 'form-control'})        