from django.contrib.auth.forms import UserCreationForm
from gestionUsuarios.forms import FormularioCrearUsuario
from registration.forms import PasswordResetForm

from django.views.generic import CreateView
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

from gestionUsuarios.models import Usuarios

# Create your views here.
class SignUpView(CreateView):
        model = Usuarios

        # deberia usar el formulario de registro que ya existe
        #form_class = UserCreationForm
        form_class = FormularioCrearUsuario
        
        #success_url = reverse_lazy('login')

       #template_name = 'registrar_usuario.html'
        template_name = 'registration/signup.html'

        #esta funcion es opcional a la variable success_url que esta mas arriba
        #pero hacerlo asi permite egregar algo por metodo get
        def get_success_url(self):
            return reverse_lazy('login') + '?registrado'



class RecuperarPassword(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    #form_class = PasswordResetForm