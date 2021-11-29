from django.contrib.auth.forms import UserCreationForm
from gestionUsuarios.forms import FormularioCrearUsuario
from registration.forms import PasswordResetForm

from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import PasswordResetView, LoginView
from django.urls import reverse
from django.urls import reverse_lazy


from gestionUsuarios.models import Usuarios



#=======================================================
# Esta clase no se usa, el registro de usuarios lo gestiona RegistrarUsuario en la app gestionUsuarios
#=======================================================
# Create your views here.
class SignUpView(CreateView):
        model = Usuarios

        # deberia usar el formulario de registro que ya existe
        #form_class = UserCreationForm
        form_class = FormularioCrearUsuario
        
        #success_url = reverse_lazy('registro_exitoso')

       #template_name = 'registrar_usuario.html'
        template_name = 'registration/signup.html'

        #esta funcion es opcional a la variable success_url que esta mas arriba
        #pero hacerlo asi permite egregar algo por metodo get
        def get_success_url(self):
            return reverse_lazy('login') + '?registro_exitoso'
            #return reverse('pppp')
            #return reverse('login', kwargs={'mensaje': 'Se ha registrado con exito.'})
            #return render(self.request, 'repairs/delete_repair.html', context) 
            #return reverse("login", {"mensaje": 'Se ha registrado con exito.'})
            #diccionario_de_contexto = {"mensaje": 'Se ha registrado con exito.'}
            #return render(self.request, "inicio.html", diccionario_de_contexto)



class RecuperarPassword(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    #form_class = PasswordResetForm


class MiLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #print("========================================")
        #print(kwargs)
        #print(self.args)
        if hasattr(self.kwargs, 'mensaje'):
            context['mensaje'] = self.kwargs['mensaje']
            print(context['mensaje'])

        return context





# =======================================================================
# REGISTRO EXITOSO ===========================================================
# =======================================================================
class RegistroExitoso(TemplateView):
    
    template_name = 'registration/registro_exitoso.html'