from django.shortcuts import render, redirect

# vistas basadas en clases
from django.views.generic import TemplateView, ListView, CreateView, View, UpdateView

# Importacion de los Modelos
from gestionStock.models import Medicamentos, Lotes

# FORMULARIOS
from gestionStock.forms import Formulario_nuevo_medicamento, Formulario_nuevo_stock

#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy



# =======================================================================
# Medicamentos ==========================================================
# =====================================================================
class ListarMedicamentos(ListView):
        model = Medicamentos
        form_class = Formulario_nuevo_medicamento
        context_object_name = "medicamentos"
        template_name = 'medicamentos.html'
        paginate_by = 100  # if pagination is desired
    #busqueda_por_farmacias = Lotes.objects.filter(ubicacion="miFarmacia")
    #busqueda_por_farmacias = Lotes.objects.filter(ubicacion__icontains="miFarmacia")



# ====================
# Buscar Medicamento =
# ==================
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
    def get_queryset(self):
        return Lotes.objects.all()
    
    # este metodo devuelve el diccionario de contexto(los datos) que va a ser enviado al template
    def get_context_data(self, **kwargs):
        diccionario_de_contexto = {}
        diccionario_de_contexto["lotes_list"] = self.get_queryset()

        #formulario_nuevo_stock
        diccionario_de_contexto["formulario_nuevo_stock"] = self.form_class
        return diccionario_de_contexto
    
    # este metodo devuelve toda la informacion cuando se hagan este tipo de peticiones
    def get(self,request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    

    def post(self,request, *args, **kwargs):
        formulario_nuevo_stock = self.form_class(request.POST)

        if formulario_nuevo_stock.is_valid():
            formulario_nuevo_stock.save()
            return redirect('stock')
        


# =======================================================================
# Editar Stock ===========================================================
# =======================================================================
class EditarStock(UpdateView):
    model = Lotes
    form_class = Formulario_nuevo_stock
    template_name = 'editar_stock.html'

    success_url = reverse_lazy('stock')




