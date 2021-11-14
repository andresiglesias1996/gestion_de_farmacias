from django.shortcuts import render, redirect
from django.urls import reverse_lazy

# vistas basadas en clases
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView, View


from gestionUsuarios.models import Usuarios, Recetas

from gestionStock.models import Farmacias, Lotes

from gestionUsuarios.forms import FormularioCrearUsuario, Formulario_nueva_receta, FormularioEditarUsuario, FormularioEditarUsuario_2, Formulario_receta_usuario

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required


#============================================================================================

#             *       *       *****      *         *          ** 
#             *       *         **           *         *        *    *
#             *       *             **       *         *       *  *  *
#             *****        *****      *****       *        * 

#============================================================================================


# =======================================================================
# Lista De Usuarios ===========================================================
# =======================================================================
class ListaDeUsuarios(ListView):
        model = Usuarios

        template_name = 'lista_de_usuarios.html'
        paginate_by = 6  # cantidad de elementos por pagina
        
        def get_queryset(self) :
                #return self.objects.filter(usuario_activo=True)
                #print(self.model.objects.filter(usuario_activo=True))
                return self.model.objects.filter(usuario_activo=True)



# =======================================================================
# Registrar Usuario ===========================================================
# =======================================================================
class RegistrarUsuario(CreateView):
        model = Usuarios
        form_class = FormularioCrearUsuario

        template_name = 'registrar_usuario.html'
        success_url = reverse_lazy('lista_de_usuarios')





# =======================================================================
# Mi Usuario | no se usa ===================================================
# =======================================================================
class MiUsuario(DetailView):

    model = Usuarios
    template_name = 'mi_usuario.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = "aca van mis variables"
        context['farmacias'] = Farmacias.objects.all()
        context['type_farmacias'] = str(type(Farmacias.objects.filter(funcionarios="101")))
        
        queryset_mi_farmacia = Farmacias.objects.filter(funcionarios="101")
        #mi_farmacia = queryset_mi_farmacia.all()[0]
        mi_farmacia = queryset_mi_farmacia[0]

        context['mi_farmacia'] = mi_farmacia
        #context['mi_farmacia'] = queryset_mi_farmacia.all()[0]
        context['stock_mi_farmacia'] =Lotes.objects.filter(ubicacion_id="1")
        

        #context['mi_farmacia'] = Farmacias.objects.filter(funcionarios="101")


        return context






# =======================================================================
# Editar Usuario ===========================================================
# =======================================================================
@method_decorator(login_required, name='dispatch')
class EditarUsuario(UpdateView):
        model = Usuarios
        form_class = FormularioEditarUsuario_2

        template_name = 'mi_usuario.html'
        success_url = reverse_lazy('mi_usuario')

        def get_object(self):
            usuario = Usuarios.objects.get(cedula_de_identidad=self.request.user.cedula_de_identidad)
            return usuario


# =======================================================================
# Editar Usuario | no se usa, esta desactivada =================
#========================================================================
@method_decorator(login_required, name='dispatch')
class ActulizarMiUsuario(UpdateView):
        model = Usuarios
        form_class = FormularioEditarUsuario_2
        #fields = ['nombre','apellido','sexo','fecha_de_nacimiento','departmento','direccion']

        success_url = reverse_lazy('mi_usuario')

        template_name = 'mi_usuario.html'

        def get_object(self):
            
            usuario, created = Usuarios.objects.get_or_create(usuario=self.request.user)
            return usuario



# =======================================================================
# Listar Recetas =========================================================
# ======================================================================
class ListarRecetas(View):
    model = Recetas
    form_class = Formulario_nueva_receta
    template_name = 'recetas.html'
    #busqueda_por_farmacias = Lotes.objects.filter(ubicacion="miFarmacia")
    #busqueda_por_farmacias = Lotes.objects.filter(ubicacion__icontains="miFarmacia")

    # este metodo devuelve la consulta principal de la vista
    def get_queryset(self):
        return Recetas.objects.all()
    
    # este metodo devuelve el diccionario de contexto(los datos) que va a ser enviado al template
    def get_context_data(self, **kwargs):
        diccionario_de_contexto = {}
        diccionario_de_contexto["recetas_list"] = self.get_queryset()

        #formulario_nuevo_stock
        diccionario_de_contexto["formulario_nueva_receta"] = self.form_class
        return diccionario_de_contexto
    
    # este metodo devuelve toda la informacion cuando se hagan este tipo de peticiones
    def get(self,request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    

    def post(self,request, *args, **kwargs):
        formulario_nueva_receta = self.form_class(request.POST)

        if formulario_nueva_receta.is_valid():

            # con esto hacemos que el formulario sea editable
            formulario_nueva_receta = formulario_nueva_receta.save(commit=False)

            # editamos el atributo medico para que el registro nuevo tenga como medico firmante al usuario que creala receta
            #luego le habilitamos el form solo a los usuarios que tienen rol == 'medico'
            formulario_nueva_receta.medico = self.request.user


            formulario_nueva_receta.save()
            return redirect('recetas')
        


# =======================================================================
# Editar Receta | creo que no se usa ========================================
# =======================================================================
class EditarReceta(UpdateView):
    model = Recetas
    form_class = Formulario_nueva_receta
    template_name = 'editar_receta.html'

    success_url = reverse_lazy('recetas')





class MisRecetas(ListView):

    #model = Usuarios
    model = Recetas
    form_class = Formulario_receta_usuario
    template_name = 'mis_recetas.html'


    def get_queryset(self):
        cedula_del_user= self.request.user.cedula_de_identidad
        queryset_mis_receta = Recetas.objects.filter(paciente=cedula_del_user)
        #mi_receta = queryset_mis_receta[0]
        return  queryset_mis_receta


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cedula_del_user = self.request.user.cedula_de_identidad

        #context['Recetas'] = Recetas.objects.all()
        #context['Usuarios'] = str(type(Usuarios.objects.filter(Usuarios='Nombre')))

        return context         
