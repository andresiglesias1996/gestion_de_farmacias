from django.db.models.query import QuerySet
from django.http import HttpResponse

# vistas basadas en clases
from django.views.generic import TemplateView, ListView, CreateView, View, UpdateView

from gestion_de_farmacias.datos_iniciales import  MEDICAMENTOS, FARMACIAS, USUARIOS, ROLES
from gestionStock.models import Medicamentos, Farmacias, Lotes
from gestionUsuarios.models import Usuarios, Recetas

#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy

# from django.template import Template, Context
import datetime
import random 
# import os
# import json
# from django.template.loader import get_template
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
# importaciones necesarias para enviar emails
from django.conf import settings
from django.core.mail import send_mail


# =====================================================================
# funciones que dan respuesta a algunas peticiones provenientes de urls.py  =
# =====================================================================


# ========
# Inicio =
# ========
class InicioView(TemplateView):

    template_name = "inicio.html"

    # aca se almacena los datos en variables que le llegan al frontend
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # verifica que la persona que accede a la pagina sea un usuario autentificado
        if self.request.user.is_authenticated and self.request.user.rol == 'farmacia':

            # si esta autentificado obtenemos el valor de la cedula de identidad del usuario
            cedula_del_user = self.request.user.cedula_de_identidad

            # con el valor de su cedula verificamos si esta registrado como funcionario de farmacia y obtenemos el dato de que farmacia es
            mis_farmacias = Farmacias.objects.filter(funcionarios=cedula_del_user)

            if len(mis_farmacias)>0:
                # pasamos el dato mi_farmacia al contexto que llega al fronend
                context['mi_farmacia'] = mis_farmacias[0]

        return context


# =====================
#  Inicio | ya no se usa =
# =====================
def inicio(request):

    diccionario_de_contexto = {"usuario": "Fulano Detail"}

    return render(request, "inicio.html", diccionario_de_contexto)


# =====================
#  SIN STOCK ===========
# =====================
def sin_stock(request):

    return render(request, "sin_stock.html")



# =================================================
# Login | la clase y la funcion siguientes ya no se usan=
# =================================================
"""class LoginPageView(TemplateView):

    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        diccionario_de_contexto = {"usuario": "Rafa"}
        return render(request, self.template_name, diccionario_de_contexto)

"""
"""def login(request):
	diccionario_de_contexto={"usuario":"Rafael Burgueño"}
	return render(request, "login.html", diccionario_de_contexto)
"""


# ===============================
# Carga de datos a la base de datos =
# ===============================
# Se ejecutan cuando cuando se accede a la ruta 'localhost/carga_medicamentos/'
# al ejecutar esta funcion se cargan registros a la tabla Medicamentos
def carga_medicamentos(request):

    for medicamento in MEDICAMENTOS:
        #print("si lee el array")
        print("-->" + str(medicamento["nombre_comercial"]))

        medicamento_nuevo = Medicamentos.objects.create(
            nombre_comercial=medicamento["nombre_comercial"],
            categoria=medicamento["categoria"],
            laboratorio=medicamento["laboratorio"],
            principio_activo=medicamento["principio_activo"],
            forma=medicamento["forma"],
            contraindicaciones=medicamento["contraindicaciones"]
        )

        medicamento_nuevo.save()

    """
     medicamento_nuevo = Medicamentos.objects.create(
            nombre_comercial=medicamento["nombre_comercial"], 
            categoria='venta libre', 
            laboratorio=medicamento["nombre_comercial"], 
            principio_activo=medicamento["nombre_comercial"], 
            forma=medicamento["nombre_comercial"], 
            contraindicaciones=medicamento["nombre_comercial"]

    
    """

    #print("paso por la funcion carga_datos")

    return redirect('medicamentos')









# =================================
# Carga Farmacias a la base de datos =
# =================================
# Se ejecutan cuando cuando se accede a la ruta 'localhost/carga_farmacias/'
# al ejecutar esta funcion se cargan registros a la tabla Farmacias
def carga_farmacias(request):

    for farmacia in FARMACIAS:
        farmacia_nueva = Farmacias.objects.create(
        #id=farmacia['id'],
        nombre=farmacia['nombre'],
        direccion=farmacia['direccion'],
        localidad=farmacia['localidad'],
        departamento=farmacia['departamento'],
        )
        farmacia_nueva.save()
        print(farmacia_nueva)

    return redirect('farmacias')





# ===============================
# Carga Usuarios a la base de datos =
# ===============================
# Se ejecutan cuando cuando se accede a la ruta 'localhost/carga_usuarios/'
# al ejecutar esta funcion se cargan registros a la tabla Usuarios
def carga_usuarios(request):

    

    for usuario in USUARIOS:
        
        usuario_nuevo = Usuarios.objects.create(
            cedula_de_identidad=usuario['cedula_de_identidad'],
            rol=ROLES[usuario["rol"]],
            usuario=usuario["usuario"],
            nombre=usuario["nombre"],
            apellido=usuario["apellido"],
            fecha_de_nacimiento=usuario["fecha_de_nacimiento"],
            email=usuario["email"],
            telefono=usuario["telefono"],
            direccion=usuario["direccion"]
        )

        usuario_nuevo.save()

    #print("paso por la funcion carga_usuaros")

    return redirect('lista_de_usuarios')








# ===============================
# Carga Lotes a la base de datos =
# ===============================
# Se ejecutan cuando cuando se accede a la ruta 'localhost/carga_usuarios/'
# al ejecutar esta funcion se cargan registros a la tabla Usuarios
def carga_stock(request):

    queryset_medicamentos = Medicamentos.objects.all()
    usuario_de_stock = Usuarios.objects.get(usuario="AndresIglesias")
    farmacia_general = get_object_or_404(Farmacias, nombre ='Farmacia General')
    #print(queryset_medicamentos)
    #print(usuario_de_stock)
    #print(farmacia_general)
    #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    
    for medicamento in queryset_medicamentos:
        
        stock_nuevo = Lotes.objects.create(
            medicamento=medicamento,
            principio_activo=medicamento.principio_activo,
            funcionario=usuario_de_stock,
            stock=random.randint(1,200),
            ubicacion=farmacia_general,
            vencimiento="2022-11-22"
        )

        stock_nuevo.save()
    
    #print("paso por la funcion carga_stock")
    #print(ROLES)

    return redirect('stock')



# ===============================
# Carga Recetas a la base de datos =
# ===============================
# Se ejecutan cuando cuando se accede a la ruta 'localhost/carga_usuarios/'
# al ejecutar esta funcion se cargan registros a la tabla Usuarios
def carga_recetas(request):
    
    queryset_medicamentos = Medicamentos.objects.all()
    usuarios = Usuarios.objects.all()
    medicos = usuarios.filter(rol="medico")
    #farmacia_general = get_object_or_404(Farmacias, nombre ='Farmacia General')

    cantidad_de_usuarios= len(usuarios)-1
    cantidad_de_medicos= len(medicos)-1

    #print(queryset_medicamentos)
    #print(aleatorio)
    #print(medico)
    #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    
    for medicamento in queryset_medicamentos:
        usuario_aleatorio = random.randint(0,cantidad_de_usuarios) # returns a random integer in the example above a <= n <= b
        medico_aleatorio = random.randint(0,cantidad_de_medicos)
        cronico_aleatorio = random.randint(0,1)
        estado_aleatorio = bool(random.randint(0,1))

        receta_nueva = Recetas.objects.create(
            principio_activo=medicamento.principio_activo,
            paciente=usuarios[usuario_aleatorio],
            medico=medicos[medico_aleatorio],
            cronico=cronico_aleatorio,
            descripcion="Nulla sollicitudin ante vel massa hendrerit. Fusce varius dolor sed ipsum egestas, non consectetur sem auctor.",
            vencimiento="2022-11-22",
            estado="RES" if estado_aleatorio else "RET"
        )
        receta_nueva.save()
    
    #print("paso por la funcion carga_stock")
    #print(ROLES)

    return redirect('recetas')
