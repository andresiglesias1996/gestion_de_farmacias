from django.shortcuts import render, redirect

# vistas basadas en clases
from django.views.generic import DetailView, TemplateView, ListView, CreateView, View, UpdateView

# Importacion de los Modelos
from gestionStock.models import Medicamentos, Lotes, Farmacias
from gestionUsuarios.models import Usuarios

# FORMULARIOS
from gestionStock.forms import Formulario_nuevo_medicamento, Formulario_nuevo_stock

#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy



# =======================================================================
# Medicamentos ==========================================================
# =====================================================================
class ListarMedicamentos(ListView):
        model = Medicamentos
        #form_class = Formulario_nuevo_medicamento
        template_name = 'medicamentos.html'

        # la siguiente linea define el nombre de la lista de elementos que se mandan al template
        context_object_name = "medicamentos"
        paginate_by = 8  # cantidad de elementos por pagina



# =============================
# Buscar Medicamento | no se usa =
# =============================
def buscar_medicamento(request):

    mensaje = ""
    diccionario_de_contexto = {
        "usuario": "Rafael Burgueño", "mensaje": mensaje}

    if request.GET["termino_buscado"]:

        termino_buscado = request.GET["termino_buscado"]

        if len(termino_buscado) > 20:
            mensaje = "El termino buscado es demasiado extenso."
            diccionario_de_contexto = {
                "usuario": "Rafael Burgueño", "mensaje": mensaje}
        else:
            # __icontains busca la palabra en elguna parte del registro
            medicamentos = Medicamentos.objects.filter(
                nombre_comercial__icontains=termino_buscado)
            # mensaje = "Se encontraron %r medicamentos" % len(medicamentos)
            diccionario_de_contexto = {"medicamentos": medicamentos,
                                       "termino_buscado": termino_buscado, "usuario": "Rafael Burgueño", "mensaje": mensaje}

    return render(request, "medicamentos.html", diccionario_de_contexto)


        
    
        

# =======================================================================
# Stock =================================================================
# =====================================================================
class Stock(View):
    model = Lotes

    form_class = Formulario_nuevo_stock
    template_name = 'stock.html'
    #busqueda_por_farmacias = Lotes.objects.filter(ubicacion="miFarmacia")
    #busqueda_por_farmacias = Lotes.objects.filter(ubicacion__icontains="miFarmacia")

    # este metodo devuelve la consulta principal de la vista
    # aca podemos manipular la consulta que la clase Stock hace a la base de datos
    def get_queryset(self):
        return Lotes.objects.all()
    
    # este metodo devuelve el diccionario de contexto(los datos) que va a ser enviado al template
    # la usamos para agregar datos que queremos hacer llegar al template
    def get_context_data(self, **kwargs):
        diccionario_de_contexto = {}
        diccionario_de_contexto["lotes_list"] = self.get_queryset()

        #le enviamos el formulario_nuevo_stock como una variabl de contecto
        diccionario_de_contexto["formulario_nuevo_stock"] = self.form_class
        return diccionario_de_contexto
    
    # este metodo se ejecuta cuando se envian peticions por GET a la pagina
    def get(self,request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    # este metodo se ejecuta cuando se envian peticions por POST a la pagina
    def post(self,request, *args, **kwargs):
        
        # copiamos a una variable los datos que llegaron del formulario
        formulario_nuevo_stock = self.form_class(request.POST)

        # verificamos que los datos esten completos o sean correctos
        if formulario_nuevo_stock.is_valid():
            
            # si todo esta bien se guardan los datos de el nuevo registro de stock
            formulario_nuevo_stock.save()
            return redirect('stock')
        


# =======================================================================
# Editar Stock ===========================================================
# =======================================================================
class EditarStock(UpdateView):
    model = Lotes
    form_class = Formulario_nuevo_stock
    template_name = 'editar_stock.html'

    success_url = reverse_lazy('mi_stock')




# =======================================================================
# Mi Stock ===========================================================
# =======================================================================
# MiStock solo muestra los registros de stock asociados a la farmacia a la que pertenezco
class MiStock(ListView):

    model = Lotes
    form_class = Formulario_nuevo_stock
    template_name = 'mi_stock.html'
    
    # aca definimos que datos queremos mostrar como una lista
    # en este caso mostramos los datos de stock de la farmacia a la que pertenece el usuario
    def get_queryset(self):
        # obtenemos la cedula del usuario
        cedula_del_user = self.request.user.cedula_de_identidad

        #con la cedula hacemos la busqueda de la Farmacia que tiene a ese usuario cono funcionario
        queryset_mi_farmacia = Farmacias.objects.filter(funcionarios=cedula_del_user)
        mi_farmacia = queryset_mi_farmacia[0]

        # con el numero id de la farmacia a la que pertenecemos
        # hacemos la busqueda de los registros de stock de esa farmacia
        stock_de_mi_farmacia = Lotes.objects.filter(ubicacion_id=mi_farmacia.id)
        
        # y retornamos solo el stock_de_mi_farmacia
        return stock_de_mi_farmacia
        
    # aca le agregamos los datos que vamos a usar en el template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # obtenemos la cedula del usuario
        cedula_del_user = self.request.user.cedula_de_identidad

        # obtenemos la farmacias a la que pertenece el usuario 
        queryset_mi_farmacia = Farmacias.objects.filter(funcionarios=cedula_del_user)
        mi_farmacia = queryset_mi_farmacia[0]
    
        
        # enviamos la farmacia y el formulario como variables de contexto
        context['mi_farmacia'] = mi_farmacia
        context["formulario_nuevo_stock"] = self.form_class

        return context



    def post(self,request, *args, **kwargs):

        # la cedula la necesito para encontrar la farmacia que le corresponde al usuario
        cedula_del_user = self.request.user.cedula_de_identidad
        mi_farmacia = Farmacias.objects.filter(funcionarios=cedula_del_user)[0]

        # cargamos el formulario que nos llega con un nuevo stock
        formulario_nuevo_stock = self.form_class(request.POST)

        # verificamos si el formulario esta bien
        if formulario_nuevo_stock.is_valid():

            # con esto hacemos que el formulario sea editable
            formulario_nuevo_stock = formulario_nuevo_stock.save(commit=False)

            
            # editamos el atributo ubicacion para que el registro nuevo tenga la ubicacion de nuestra farmacia
            formulario_nuevo_stock.ubicacion = mi_farmacia

            #guardamos el registro del formularios
            formulario_nuevo_stock.save()

            return redirect('mi_stock')
        
        #return redirect('mi_stock')


