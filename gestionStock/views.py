from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.db.models import Sum
# re-cableando la mente
# vistas basadas en clases
from django.views.generic import DetailView, TemplateView, ListView, CreateView, View, UpdateView

# Importacion de los Modelos
from gestionStock.models import Medicamentos, Lotes, Farmacias
from gestionUsuarios.models import Usuarios, Recetas

# FORMULARIOS
from gestionStock.forms import Formulario_nueva_farmacia ,Formulario_nuevo_medicamento, Formulario_nuevo_stock, Formulario_nuevo_stock_con_farmacias

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
        #paginate_by = 8  # cantidad de elementos por pagina



# =======================================================================
# Farmacias =============================================================
# =====================================================================
class ListarFarmacias(ListView):
        model = Farmacias
    
        template_name = 'farmacias.html'

        context_object_name = "farmacias"
        #paginate_by = 10  

        def get_queryset(self):
                #con el filter(receta_de_destino=None) traemos los registros que no estan asignados a ninguna receta
                #los registros despachados quedan registrados como registros negativos y con un objeto Recetas en la variable receta_de_destino
                return Farmacias.objects.exclude(nombre='Farmacia General')




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
        #con el filter(receta_de_destino=None) traemos los registros que no estan asignados a ninguna receta
        #los registros despachados quedan registrados como registros negativos y con un objeto Recetas en la variable receta_de_destino
        return Lotes.objects.all()
    
    # este metodo devuelve el diccionario de contexto(los datos) que va a ser enviado al template
    # la usamos para agregar datos que queremos hacer llegar al template
    def get_context_data(self, **kwargs):
        diccionario_de_contexto = {}
        diccionario_de_contexto["lotes_list"] = self.get_queryset()

        #le enviamos el formulario_nuevo_stock como una variabl de contecto
        diccionario_de_contexto["formulario_nuevo_stock"] = self.form_class
        #===============================================================
            #STOCK ACUMULADO
            #este algoritmo va a ser muy ineficiente XD
        #===============================================================
        #mi_farmacia =get_object_or_404(Farmacias, funcionarios=self.request.user.cedula_de_identidad)
        mis_farmacias = Farmacias.objects.filter(funcionarios=self.request.user.cedula_de_identidad)
        #print(mis_farmacias)
        if len(mis_farmacias) < 1:
            #print("el usuario no esta en ninguna farmacia")
            #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            diccionario_de_contexto["no_esta_autorizado"] = "No esta autorizado a ver el stock."
        else:
            mi_farmacia = mis_farmacias[0]
        
            queryset_stock_total_mi_farmacia = Lotes.objects.filter(ubicacion_id=mi_farmacia.id)

            stock_acumulado = []

            for cada_registro_de_stock_de_mi_farmacia in queryset_stock_total_mi_farmacia:
                
                stock_acumulado_del_medicamento = 0

                registros_stock_duplicados = queryset_stock_total_mi_farmacia.filter(medicamento=cada_registro_de_stock_de_mi_farmacia.medicamento.id)
                
                
                #este for suma los valores y los pone en la variablestock_acumulado_de_medicamentos
                for registro in registros_stock_duplicados:
                    stock_acumulado_del_medicamento += registro.stock
                
                if not stock_acumulado.__contains__({"medicamento":cada_registro_de_stock_de_mi_farmacia.medicamento,"stock":stock_acumulado_del_medicamento}):
                    stock_acumulado.append({"medicamento":cada_registro_de_stock_de_mi_farmacia.medicamento,"stock":stock_acumulado_del_medicamento})
            
                

                #context['stock_acumulado']= queryset_stock_total.filter(medicamento=96)
                diccionario_de_contexto['stock_acumulado']= stock_acumulado
        
        return diccionario_de_contexto
    
    # este metodo se ejecuta cuando se envian peticions por GET a la pagina
    def get(self,request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    # este metodo se ejecuta cuando se envian peticions por POST a la pagina
    def post(self,request, *args, **kwargs):
        
        # copiamos a una variable los datos que llegaron del formulario
        formulario_nuevo_stock = self.form_class(request.POST)

        id_medicamento=request.POST.get('medicamento')
        medicamento = Medicamentos.objects.get(id=id_medicamento)
        mi_farmacia = Farmacias.objects.filter(funcionarios=request.user.cedula_de_identidad)[0]

        # verificamos que los datos esten completos o sean correctos
        if formulario_nuevo_stock.is_valid():
            
            # con esto hacemos que el formulario sea editable
            formulario_nuevo_stock = formulario_nuevo_stock.save(commit=False)

            formulario_nuevo_stock.funcionario = self.request.user
            formulario_nuevo_stock.principio_activo = medicamento.principio_activo
            formulario_nuevo_stock.ubicacion = mi_farmacia


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
        #queryset_mi_farmacia = get_list_or_404(Farmacias, funcionarios=cedula_del_user)
        #print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
        #print("el len(queryset_mi_farmacia) dice: vvvv")
        #print(len(queryset_mi_farmacia))
        
        if len(queryset_mi_farmacia)>0:
            mi_farmacia = queryset_mi_farmacia[0]

        # con el numero id de la farmacia a la que pertenecemos
        # hacemos la busqueda de los registros de stock de esa farmacia
            stock_de_mi_farmacia = Lotes.objects.filter(ubicacion_id=mi_farmacia.id)
        
        # y retornamos solo el stock_de_mi_farmacia
            return stock_de_mi_farmacia
        
        return {"mensaje":"El funcionario de farmacia no tiene ninguna farmacia asignada"}


    # aca le agregamos los datos que vamos a usar en el template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # obtenemos la cedula del usuario
        cedula_del_user = self.request.user.cedula_de_identidad

        # obtenemos la farmacias a la que pertenece el usuario 
        queryset_mi_farmacia = Farmacias.objects.filter(funcionarios=cedula_del_user)
        if len(queryset_mi_farmacia)>0:
            mi_farmacia = queryset_mi_farmacia[0]
            # enviamos la farmacia y el formulario como variables de contexto
            context['mi_farmacia'] = mi_farmacia

    




#===============================================================
            #STOCK ACUMULADO
            #este algoritmo va a ser muy ineficiente XD
#===============================================================
            queryset_stock_total_mi_farmacia = Lotes.objects.filter(ubicacion_id=mi_farmacia.id)

            stock_acumulado = []

            for cada_registro_de_stock_de_mi_farmacia in queryset_stock_total_mi_farmacia:
                #print("=================REGISTRO DE STOCK ====================")
                #print(cada_registro_de_stock_de_mi_farmacia.medicamento.id)
                stock_acumulado_del_medicamento = 0

                registros_stock_duplicados = queryset_stock_total_mi_farmacia.filter(medicamento=cada_registro_de_stock_de_mi_farmacia.medicamento.id)
                # returns {'price__sum': 1000} for example
                
                #este for suma los valores y los pone en la variablestock_acumulado_de_medicamentos
                for registro in registros_stock_duplicados:
                    stock_acumulado_del_medicamento += registro.stock
                
                if not stock_acumulado.__contains__({"medicamento":cada_registro_de_stock_de_mi_farmacia.medicamento,"stock":stock_acumulado_del_medicamento}):
                    stock_acumulado.append({"medicamento":cada_registro_de_stock_de_mi_farmacia.medicamento,"stock":stock_acumulado_del_medicamento})
                #print(cada_registro_de_stock_de_mi_farmacia)
                #print(type(cada_registro_de_stock_de_mi_farmacia.medicamento))
                #stock_acumulado.append({"medicamento":cada_registro_de_stock_de_mi_farmacia.medicamento,"stock":stock_acumulado_del_medicamento})
                #con esto logro crear una tabla de tuplas (id_medicamento, stock_acumulado_de_mi_farmacia)

            #print("=================MEDICAMENTO===========AAAA====")
            #stock_acumulado = list(set(stock_acumulado))
            #print(stock_acumulado)
            #print(type(stock_acumulado))




                #print("======registro_de_stock=======")
                #print(type(registro_de_stock)) #devuelve -> <class 'gestionStock.models.Lotes'>
                #print(registro_de_stock.medicamento)
            #if registro_de_stock.medicamento == 96:
                #context['stock_acumulado']=registro_de_stock.medicamento
                    #print("encontre el 96 :")
                    #print( registro_de_stock.medicamento)
                

            #context['stock_acumulado']= queryset_stock_total.filter(medicamento=96)
            context['stock_acumulado']= stock_acumulado
            
            #print(len(context['stock_acumulado']))
            #print(context['stock_acumulado'])
        





        context["formulario_nuevo_stock"] = self.form_class

        return context



    def post(self,request, *args, **kwargs):

        # la cedula la necesito para encontrar la farmacia que le corresponde al usuario
        cedula_del_user = self.request.user.cedula_de_identidad
        formulario_nuevo_stock = self.form_class(request.POST)
        #medicamento=request.POST.get('id_stock')
        id_medicamento=request.POST.get('medicamento')
        medicamento = Medicamentos.objects.get(id=id_medicamento)
        farmacia_general=Farmacias.objects.get(nombre='Farmacia General')

        #medicamento=formulario_nuevo_stock.get('id_medicamento')
        #request.POST.get('id_receta')
        #print(farmacia_general)
        #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

        mi_farmacia = Farmacias.objects.filter(funcionarios=cedula_del_user)[0]

        # cargamos el formulario que nos llega con un nuevo stock
        #print(type(formulario_nuevo_stock.id_medicamento))
        # verificamos si el formulario esta bien
        if formulario_nuevo_stock.is_valid():
            if mi_farmacia.id != farmacia_general.id:
                
                #este algoritmo va a revisar si hay stock del medicamento en la farmacia Central
                #si no hay : primero evita que se generen registros negativos
                queryset_lotes_del_medicamento_en_deposito = Lotes.objects.filter(medicamento=medicamento)
                #queryset_lotes_del_medicamento_en_deposito = get_list_or_404(Lotes, medicamento=medicamento)
                
                if len(queryset_lotes_del_medicamento_en_deposito)<1:
                    #return reverse_lazy('login') + '?registro_exitoso'
                    #return reverse_lazy('mi_stock') + '?sin_stock'
                    #================================================
                    #=================TODO ==========================
                    # avisar al funcionario de 
                    # farmacia que no puede hacer el stock porque no hay 
                    # stock en la farmacia general======================
                    #================================================
                    return redirect('sin_stock')
                    #por ahora solo redirecciona de regreso a mi_stock

                else:
                    stock_en_deposito = 0
                    for registro in queryset_lotes_del_medicamento_en_deposito:
                        stock_en_deposito += registro.stock
                    
                    if stock_en_deposito <= int(request.POST.get('stock')):
                        #================================================
                        #=================TODO ==========================
                        # avisar al funcionario de 
                        # farmacia que no puede hacer el stock porque no hay 
                        # stock en la farmacia general======================
                        #================================================
                        return redirect('sin_stock')





                Lotes.objects.create(
                    medicamento=medicamento,
                    principio_activo=medicamento.principio_activo,
                    funcionario=self.request.user,
                    stock= -int(request.POST.get('stock')),
                    ubicacion=farmacia_general,
                    vencimiento=request.POST.get('vencimiento')
                    ) 
               
            #medicamento = Medicamentos.objects.get(id=medicamento)
            #print(medicamento)

            # con esto hacemos que el formulario sea editable
            formulario_nuevo_stock = formulario_nuevo_stock.save(commit=False)

            # editamos el atributo funcionario para que el registro nuevo tenga como funcionario firmante al usuario que ingresa el registro de stock
            #luego le habilitamos el form solo a los usuarios que tienen rol == 'farmacia'
            formulario_nuevo_stock.funcionario = self.request.user

            formulario_nuevo_stock.principio_activo = medicamento.principio_activo
            
            # editamos el atributo ubicacion para que el registro nuevo tenga la ubicacion de nuestra farmacia
            formulario_nuevo_stock.ubicacion = mi_farmacia

            #guardamos el registro del formularios
            formulario_nuevo_stock.save()

            return redirect('mi_stock')
        #else :
            #context = self.get_context_data()
            #context["formulario_nuevo_stock"] = formulario_nuevo_stock
            #return render(request, 'mi_stock.html', context)
            #return redirect('mi_stock')

        #return redirect('mi_stock')
        #context= {}
        #context["formulario_nuevo_stock"] = formulario_nuevo_stock
        #return render(request,'mi_stock.html', context)




# =======================================================================
# Gestionar Receta ===========================================================
# =======================================================================
class GestionarReceta(TemplateView):
    
    template_name = 'gestionar_receta.html'

    #success_url = reverse_lazy('lista_de_usuarios')

    # recopilamos los datos que se van a mostrar en la vista
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cedula_del_funcionario = self.request.user.cedula_de_identidad

        # obtenemos la farmacias a la que pertenece el usuario 
        queryset_mi_farmacia = Farmacias.objects.filter(funcionarios=cedula_del_funcionario)
        
        #print("================================")
        #print(queryset_mi_farmacia)
        if len(queryset_mi_farmacia)==0:
            context['mensaje'] = "Su usuario no esta asignado a ninguna farmacia."
            return context

        #obtenemos de la url el numero de receta que queremos consultar
        numero_de_receta =self.kwargs['pk']
        #buscamos la receta en la base de datos con el fin de obtener el principio_activo que se ha recetado
        #queryset_recetas = Recetas.objects.filter(id=numero_de_receta)
        context['receta'] = Recetas.objects.get(id=numero_de_receta)
        usuario_del_paciente = context['receta'].paciente
        #paciente = Usuarios.objects.get(usuario=usuario_del_paciente)
        paciente = get_object_or_404(Usuarios, usuario=usuario_del_paciente)
        context['paciente'] = paciente

        #obtenemos el principio activo
        principio_activo = context['receta'].principio_activo
        #ya con el principio activo buscamos los medicamentos que satisfacen a esa receta
        queryset_opciones_de_medicamentos = Medicamentos.objects.filter(principio_activo=principio_activo)
        queryset_con_stock = Lotes.objects.filter(ubicacion=queryset_mi_farmacia[0].id).filter(principio_activo=principio_activo)

        opciones_con_info_de_stock = []
        for medicamento in  queryset_opciones_de_medicamentos:
            #aca iria el codigo para revisar si existe stock de ese medicamento
            stock_disponible =False
            registro_de_stock_del_medicamento= queryset_con_stock.filter(medicamento=medicamento.id)
            if len(registro_de_stock_del_medicamento) > 0:
                
                cantidad_acumulada_del_medicamento_en_mi_farmacia = 0
                for registro in registro_de_stock_del_medicamento:
                    cantidad_acumulada_del_medicamento_en_mi_farmacia += registro.stock

                #print("VVVVVVVVVVVVVVcantidadacumulada del medicamentoVVVVVVVVVVVVVVVVVVV")
                #print(cantidad_acumulada_del_medicamento_en_mi_farmacia)


                if cantidad_acumulada_del_medicamento_en_mi_farmacia > 0:
                    stock_disponible = True

            opciones_con_info_de_stock.append([medicamento, stock_disponible])


        #print("==========================================================")
        #print(queryset_con_stock)
        #print(opciones_con_info_de_stock)
        #context['opciones_de_medicamentos'] =queryset_opciones_de_medicamentos
        context['opciones_de_medicamentos'] =opciones_con_info_de_stock

        
        #if len(queryset_recetas) > 0:
            #context['receta'] = queryset_recetas[0]
        

        return context





    #======================================================================
    #============================POST==================================
    #======================================================================
    #con este metodo capturamos la interaccion para despachar algun medicamento especifico
    def post(self,request, *args, **kwargs): 

        #obtenemos el id del medicamento que se elije despachar
        id_medicamento_entregado=request.POST.get('id_medicamento')
        id_receta_entregada=request.POST.get('id_receta')
        cedula_del_paciente=int(request.POST.get('cedula_del_paciente'))
        
        #la cedula la necesitamos para buscar la farmacia del funcionario que realiza la gestion
        cedula_del_user = self.request.user.cedula_de_identidad
        #queryset_mi_farmacia = Farmacias.objects.filter(funcionarios=cedula_del_user)
        queryset_mi_farmacia = get_list_or_404(Farmacias, funcionarios=cedula_del_user)
        #print("===============================")
        #print(cedula_del_user)
        #este if previene un error generado cuando el funcionario no esta asignado a ninguna farmacia
        if len(queryset_mi_farmacia)>0:
            #obtenemos el object que representa a nuestra farmacia
            mi_farmacia = queryset_mi_farmacia[0]
            
            #buscamos en el stock de nuestra farmacia, todos los registro de ese medicamentos
            #con el fin de restar un elemento al registro
            #uticizamos .order_by('-created') para que el queryset nos llegue con los registros antiguos primero
            queryset_stock_de_mi_farmacia = Lotes.objects.filter(ubicacion_id=mi_farmacia.id).filter(medicamento=id_medicamento_entregado).order_by('created')
            
            #con este if prevenimos el error generado al no encontrar registros de stock para ese medicamento
            if len (queryset_stock_de_mi_farmacia)>0:   
                registro_de_stock_que_satisface_la_receta = queryset_stock_de_mi_farmacia[0]
                #print("====================medicamento_entregado==========================")
                #print(type(registro_de_stock_que_satisface_la_receta))
                #analizamos cada registro para encontras stock positivo de donde restar el medicamento entregado
                """
                #comente este bucle for para que la actulizacion del stock sea con un registro negativo 
                # y no modificando un registro existente
                for registro in queryset_stock_de_mi_farmacia:
                    if registro.stock > 0:
                        registro.stock = registro.stock -1
                        registro.save()
                        break
                """
                #con esto elegimos el ultimo registro de lote para restar el medicamento entregado
                #stock_de_mi_farmacia = queryset_stock_de_mi_farmacia[len(queryset_stock_de_mi_farmacia)-1]
                #stock_de_mi_farmacia.stock = stock_de_mi_farmacia.stock - 1

                #finalmente les restamos 1 al registro esto significa el ql medicamento fue entregado 
                medicamento_entregado =  Medicamentos.objects.get(id=id_medicamento_entregado)
                funcionario =  Usuarios.objects.get(cedula_de_identidad=cedula_del_user)
                principio_activo_del_medicamento_entregado =medicamento_entregado.principio_activo
                receta_de_destino =  Recetas.objects.get(id=id_receta_entregada)
                
                #print(medicamento_entregado)
                #print(type(medicamento_entregado))
                #print(receta_de_destino.id)
                #print(principio_activo_del_medicamento_entregado)
                #stock_de_mi_farmacia.save()
                Lotes.objects.create(
                    medicamento=medicamento_entregado,
                    principio_activo=principio_activo_del_medicamento_entregado,
                    funcionario=funcionario,
                    stock=-1,
                    ubicacion=mi_farmacia,
                    receta_de_destino=receta_de_destino,
                    vencimiento=registro_de_stock_que_satisface_la_receta.vencimiento
                    )
                #si todo va bien, podemos cambiar el estado a retirado(RET)
                #obtenemos el id de la receta y actualizamos su estado
                if receta_de_destino.cronico == False:
                    #receta_de_destino.estado='RET'

                    Recetas.objects.filter(id=id_receta_entregada).update(estado='RET')

        #return reverse('article_details', args=(pk, slug))
        #return  redirect('recetas_usuario/'+cedula_del_paciente + '/') 
        return redirect('recetas_usuario', pk=cedula_del_paciente)
        #return  redirect('lista_de_usuarios')
        #return reverse('recetas_usuario', args=([cedula_del_paciente]))





# =======================================================================
# InfoDelMedicamento ==========================================
# =======================================================================
class InfoDelMedicamento(TemplateView):
    #model = Farmacias
    template_name = 'info_del_medicamento.html'

    #context_object_name = "farmacias"
    #pass
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
         #Farmacias.objects.get(id=numero_de_receta)

        id_medicamento =self.kwargs['pk']
        medicamento=Medicamentos.objects.get(id=id_medicamento)
        context['medicamento'] = medicamento

        farmacia_general = Farmacias.objects.get(nombre="Farmacia General")

        queryset_registros_de_stock = Lotes.objects.filter(medicamento=id_medicamento).exclude(ubicacion=farmacia_general)
        farmacias_con_stock = []
        for registro in queryset_registros_de_stock:
            farmacias_con_stock.append( registro.ubicacion )

        #elimino las farmacias duplicadas
        farmacias_con_stock= list(set(farmacias_con_stock))
        #farmacias_con_stock= Farmacias.objects.all()

        ubicacion_y_stock=[]
        for farmacia in farmacias_con_stock:

            ubicacion_y_stock.append( [farmacia, farmacia.consultar_stock_acumulado(id_medicamento)] )
            


        #print("=================queryset REGISTROs DE STOCK ====================")
        #print(ubicacion_y_stock)
                
        context['farmacias'] = ubicacion_y_stock
        #context['farmacias'] = Farmacias.objects.all()

        return context

class CrearFarmacia(CreateView):
        model = Farmacias
        form_class = Formulario_nueva_farmacia

        template_name = 'crear_farmacia.html'
        #success_url = reverse_lazy('login')
    
        def get_success_url(self):
                return reverse_lazy('farmacias') + '?registro_exitoso'

class EditarFarmacia(UpdateView):
    model = Farmacias
    form_class = Formulario_nueva_farmacia
    template_name = 'editar_farmacia.html'

    def get_success_url(self):
        return reverse_lazy('farmacias') + '?registro_exitoso'
