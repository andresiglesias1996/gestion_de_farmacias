from django.db.models.query import QuerySet
from django.http import HttpResponse

# vistas basadas en clases
from django.views.generic import TemplateView, ListView, CreateView, View, UpdateView

from gestionStock.models import Medicamentos, Farmacias
from gestionUsuarios.models import Usuarios

#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy

# from django.template import Template, Context
import datetime
# import os
# import json
# from django.template.loader import get_template
from django.shortcuts import render, redirect

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

    # print("el request.user.rol.nombre dice: " + str(request.user.rol.nombre) )
    # json_personas= json.dumps(lista_personas)
    # json_personas= json.dumps([11,12,13,14,15])
    json_personas = [11, 12, 13, 14, 15]

    diccionario_de_contexto = {"usuario": "Fulano Detail"}

    return render(request, "inicio.html", diccionario_de_contexto)


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
            categoria='venta libre',
            laboratorio=medicamento["laboratorio"],
            principio_activo=medicamento["nombre_comercial"],
            forma="comprimidos",
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


"""
###################################################################
plantilla para generar los datos en: https://www.json-generator.com/
###################################################################
[
  '{{repeat(5, 7)}}',
  {
    nombre_comercial: '{{surname()}}{{integer(100, 999)}}',
    laboratorio: '{{company().toUpperCase()}}',
    contraindicaciones: '{{lorem(1, "paragraphs")}}'
  }
]
"""

MEDICAMENTOS = [
{
    'nombre_comercial':'AAS',  
    'laboratorio':'OPELLA HEALTHCARE', 
    'principio_activo':'Acetilsalicílico ácido',                   
    'forma':'Comprimidos',  
    'contraindicaciones':'No contraindicado',                              
    'categoria':'RC'
    },
{
    'nombre_comercial':'ATROVENT NASAL',
    'laboratorio':'OPELLA HEALTHCARE',        
    'principio_activo':'Ipratropio bromuro',                        
    'forma':' PULVERIZACION NASAL',                   
    'contraindicaciones':'Hipersensibilidad a análogos de atropina.',
    'categoria': 'VL'
    },
{
    'nombre_comercial':'BISOLVON MUCOLITICO' ,     
    'laboratorio':'OPELLA HEALTHCARE',        
    'principio_activo':'Bromhexina hidrocloruro',                 
    'forma':'JARABE',                                              
    'contraindicaciones':'Hipersensibilidad.',  
    'categoria':'VL'
    },
{
    'nombre_comercial':'BUSCAPINA 10',            
    'laboratorio':'OPELLA HEALTHCARE',        
    'principio_activo':'Escopolamina butilbromuro'  ,                  
    'forma':'Comprimidos',                                         
    'contraindicaciones':'Hipersensibilidad, glaucoma de ángulo estrecho no tratado, hipertrofia prostática', 
    'categoria':'VL'
    },
{
    'nombre_comercial':'TELFAST 120',               
    'laboratorio': 'OPELLA HEALTHCARE' ,      
    'principio_activo':'Fexofenadina hidrocloruro'  ,                 
    'forma': 'Comprimidos',                                       
    'contraindicaciones':  'Hipersensibilidad' ,
    'categoria':'RC'
    },
{
    'nombre_comercial':'ABACAVIR/LAMIVUDINA 600' ,
       'laboratorio':'MYLAN PHARMACEUTICALS',  
       'principio_activo': 'Abacavir sulfato, Lamivudina',               
       'forma' :'Comprimidos',                                         
       'contraindicaciones': 'Hipersensibilidad  individuales. I.H. grave', 
       'categoria':'RC'
       },
{
    'nombre_comercial':'ABICREM 0,25 GALENICUM',     
    'laboratorio': 'DERMA S.L.',             
    'principio_activo':'Fluocinolona acetónido, Framicetina sulfato',
    'forma':  'Crema',                                           
    'contraindicaciones': 'Hipersensibilidad a sus componentes; infecciones cutáneas víricas y tuberculosas en actividad; úlceras de las extremidades; niños < 2 años', 
    'categoria':  'VL'
    },
{
    'nombre_comercial':'ABILIFY 1 MG',               
    'laboratorio':'OTSUKA PHARMACEUTICAL',    
    'principio_activo': 'Aripiprazol' ,                             
    'forma' :'Solucion Oral',                                       
    'contraindicaciones': 'Hipersensibilidad a aripiprazol',
    'categoria':  'VL'
    },
{
    'nombre_comercial':'ACARBOSA FARMALIDER 100',    
    'laboratorio':  'FARMALIDER',            
    'principio_activo':'Acarbosa',                                  
    'forma': 'Comprimidos' , 
    'contraindicaciones': 'Hipersensibilidad a los componentes de la planta',                                     
    'categoria': 'RC'
    },
{
    'nombre_comercial':'ACTITHIOL MUCOLITICO INFANTIL 20 MG',  
    'laboratorio':'lacer' ,         
    'principio_activo':'Carbocisteína Carbocisteína',             
    'forma':'Solucion Oral'    ,                                     
    'contraindicaciones':'Hipersensibilidad a la carbocisteína, a otros compuestos relacionados con la cisteína o a alguno de los excipientes Pacientes con úlcera gastroduodena' ,
    'categoria':'RC'
    },
{
    'nombre_comercial':'ADIAVAL 1.000 MG',           
    'laboratorio':'LACER',                    
    'principio_activo':'Calcio carbonato, Colecalciferol',         
    'forma':'Comprimidos Masticables',                          
    'contraindicaciones':'Hipersensibilidad. situaciones que dan lugar a hipecalcemiahipercalcemia y/o hipercalciuria; cálculos renales',  
    'categoria':'RC'
    },
{
    'nombre_comercial':'AGIOLAX GRANULADO',         
    'laboratorio':'MYLAN PHARMACEUTICALS'   ,   
    'principio_activo':'Plantago ovata forskk'   ,                 
    'forma':'semilla,  Granulado', 
    'contraindicaciones':'Hipersensibilidad, obstrucción y estenosis intestinal, íleo paralítico, enf. inflamatoria de colon' ,
    'categoria':'RC'
    },
{
    'nombre_comercial':'BECLOFORTE 250',           
    'laboratorio':'GLAXOSMITHKLINE, S.A.' ,     
    'principio_activo':'Beclometasona dipropionato'  ,                
    'forma':'Inhalador',                                    
     'contraindicaciones':'Hipersensibilidad' ,
     'categoria':'RC'
     },
{
    'nombre_comercial':'BENZETACIL 1.200.000 UI' ,   
    'laboratorio':'REIG JOFRE'  ,               
    'principio_activo':'Bencilpenicilina benzatina' ,                 
    'forma':'POLVO PARA SUSPENSIÓN INYECTABLE',
    'contraindicaciones': 'Hipersensibilidad', 
    'categoria':'RC'
    },
{
    'nombre_comercial':'BICALUTAMIDA BLUEFISH 150'  , 
    'laboratorio':'PHARMA SLU'    ,            
    'principio_activo':'Bicalutamida'   ,                               
    'forma':'Comprimidos',                            
    'contraindicaciones':'Hipersensibilidad.antecedentes de toxicidad hepática asociada con bicalutamida, concomitancia de terfenadina, astemizol o cisaprida',  
    'categoria':'RC'
    },
{
    'nombre_comercial':'BISOLFREN 200' ,           
    'laboratorio':'OPELLA HEALTHCARE' , 
    'forma':'Comprimidos',           
    'principio_activo':'Ibuprofeno, Pseudoefedrina hidrocloruro EXC: Carboximetilalmidón sódico','forma':  'Comprimidos' ,        
    'contraindicaciones':'Hipersensibilidad', 
    'categoria':'RC'
    },
{
    'nombre_comercial':'lantus 100 U/mL' ,           
    'laboratorio':'Sanofi'          ,           
    'principio_activo':'Insulina glargina'  ,                          
    'forma':'solución inyectable' ,                           
    'contraindicaciones':  'Hipersensibilidad' , 
    'categoria':'FNR'
    },
{
    'nombre_comercial':'dyslor 500 U',
    'laboratorio': 'Roemmers-Iclos',  
    'principio_activo':'Toxina botulinica', 
    'forma':  'solucion inyectable' , 
    'contraindicaciones':'Hipersensibilidad', 
    'categoria':'FNR'
    },
{
    'nombre_comercial':'tacrolimus sandoz 1 mg'  ,    
    'laboratorio':'Scienza-Novartis' ,         
    'principio_activo':'Tacrolimús'  ,                                  
    'forma':'Capsula'     ,                                
    'contraindicaciones':'Hipersensibilidad a tacrolimús o a otros macrólidos',
    'categoria':  'FNR'
    },
{
    'nombre_comercial':'CERTICAN Comprimido 0.75 mg',  
    'laboratorio':'Scienza-Novartis',         
    'principio_activo': 'Everolimus'   ,                                 
    'forma':'Comprimidos'   ,                              
    'contraindicaciones':'Hipersensibilidad a everolimús y sirolimús.' ,
    'categoria':'FNR'
    },
{
    'nombre_comercial':'AVONEX EN JERINGA PRELLENADA', 
    'laboratorio':'Biogen Idec'  ,             
    'principio_activo':'Interferón beta-1a'  ,                            
    'forma': 'Inyectable'  ,                               
    'contraindicaciones':'Hipersensibilidad a interferón-ß natural o recombinante; embarazo; depresión grave activa y/o ideación suicida', 
    'categoria':'FNR'},
{
    'nombre_comercial':'quetipax 200 mg',               
    'laboratorio':'Roemmers-Rowe'  ,          
    'principio_activo':'Quetiapina'   ,                                  
    'forma':'Comprimidos'  ,                                    
    'contraindicaciones':'Hipersensibilidad a quetiapina, concomitante con inhibidores del citocromo P450 3A4 (como inhibidores de la proteasa del VIH, antifúngicos tipo azol, eritromicina, claritromicina y nefazodona' ,
    'categoria': 'RV'
    },
{
    'nombre_comercial':'ondil 2 mg',                 
    'laboratorio':'Roemmers-Rowe' ,              
    'principio_activo':  'Alprazolam'  ,                                  
    'forma':'Comprimidos',                                 
    'contraindicaciones':'Hipersensibilidad a alprazolam, a benzodiazepinas, miastenia gravis, insuf. Respiratoria grave, síndrome de apnea del sueño',  
    'categoria':'RV'
    },
{
    'nombre_comercial':'bropan 12 mg',               
    'laboratorio':'Fármaco Uruguayo',            
    'principio_activo':'Bromazepam'   ,                                
    'forma':'Comprimidos' ,                                    
    'contraindicaciones':'Hipersensibilidad a bromazepam, a benzodiazepinas, miastenia gravis',
    'categoria': 'RV'
    },
{
    'nombre_comercial':'DALGION Gotas' ,               
    'laboratorio':'Gramón Bagó' ,                
    'principio_activo':'Tramadol'   ,                                     
    'forma':   'Gotas',                                     
    'contraindicaciones':'Hipersensibilidad a tramadol; intoxicación aguda o sobredosis con depresores del SNC (alcohol, hipnóticos, otros analgésicos opiáceos', 
    'categoria':'RV'
    },
{
    'nombre_comercial':'Aceprax',                        
    'laboratorio':'Celsius' ,                 
    'principio_activo':'Alprazolam'  ,                                
    'forma':'Comprimidos',                                       
    'contraindicaciones':'Hipersensibilidad a alprazolam, a benzodiazepinas, miastenia gravis, insuf. Respiratoria grave, síndrome de apnea del sueño',  
    'categoria':'RV'
    },
{
    'nombre_comercial':'TRAPAX',                       
    'laboratorio':'Roemmers-Rowe',                
    'principio_activo':'Lorazepam'  ,                              
    'forma':'Comprimidos',                                       
    'contraindicaciones':'Hipersensibilidad, miastenia gravis, síndrome de apnea del sueño, insuf. respiratoria severa, I.H. severa, tto. simultáneo con opiáceos, barbitúricos, neurolépticos' ,
    'categoria':'RV'},
{
    'nombre_comercial':'abretia 40 mg',                 
    'laboratorio':'Roemmers',                   
    'principio_activo':'Atomoxetina',                                  
    'forma':'Capsula',                                      
    'contraindicaciones':'Hipersensibilidad atomoxetina . Tto. concomitante con IMAO; distanciar al menos 2 sem. Glaucoma de ángulo estrecho', 
    'categoria':'RV'
    },
{
    'nombre_comercial':'ezentius 20 mg',                 
    'laboratorio':'Roemmers'  ,               
    'principio_activo':'Escitalopram',                               
    'forma':'Comprimidos',                                    
    'contraindicaciones':'Hipersensibilidad, con antecedentes de intervalo QT alargado o síndrome congénito del segmento QT largo, tto. concomitante con IMAO no selectivos irreversibles, con IMAO A reversibles',  
    'categoria':'RV'
    },
{
    'nombre_comercial':'Mizapin  ',                        
    'laboratorio':'Dispert',              
    'principio_activo': 'Mirtazapina',                                
    'forma':'Comprimidos' ,                                    
    'contraindicaciones':'Hipersensibilidad. Uso concomitante con IMAO', 
    'categoria':'RV'
    },
{
    'nombre_comercial':'NOVEMINA CON CODEINA FORTE',   
    'laboratorio':'Lazar',                      
    'principio_activo':'Codeína y otros analgésicos no opiáceos', 
    'forma':'Comprimidos',                                         
    'contraindicaciones':'Hipersensibilidad' ,
    'categoria':  'RV'
    }
]




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

    return redirect('farmacias')

FARMACIAS = [
{'nombre':'Montevideo Central'  , 'departamento':'Montevideo', 'direccion':   '18 de julio 1234', 'localidad':'  Montevideo'},
{'nombre':'Montevideo Curva de Maroñas' , 'departamento':'Montevideo', 'direccion':   '8 de octubre 1234', 'localidad':' Montevideo'},
{'nombre':'Montevideo Pocitos'  , 'departamento':'Montevideo', 'direccion':   'Tezanos 1234', 'localidad':'  Montevideo'},
{'nombre':'Montevideo Cerro'  , 'departamento':'Montevideo', 'direccion':   'Rusia 1234', 'localidad':'  Montevideo'},
{'nombre':'Montevideo Prado'  , 'departamento':'Montevideo', 'direccion':   'Millan 1234', 'localidad':' Montevideo'},
{'nombre':'Canelones Zona Sur'  , 'departamento':'Canelones', 'direccion':  'Las violetas 2345', 'localidad':' Pando'},
{'nombre':'San Jose Oeste'  , 'departamento':'San Jose', 'direccion':   'Miraflores 3456', 'localidad':' Libertad'},
{'nombre':'Maldonado Central' , 'departamento':'Maldonado', 'direccion':  'Dr Puey 3456', 'localidad':'  Maldonado'},
{'nombre':'Canelones Central' , 'departamento':'Canelones', 'direccion':  'Edison 5645', 'localidad':' Canelones'},
{'nombre':'  Maldonado  Norte'  , 'departamento':'Maldonado', 'direccion':  'Los ceibos 2345', 'localidad':' Aigua'},
{'nombre':'  San Jose Central'  , 'departamento':'San Jose', 'direccion':   'Avda Gutierrez', 'localidad':' 4567', 'localidad':' San Jose'},
{'nombre':'  Durazno Central' , 'departamento':'Durazno', 'direccion':  'Juan Carlos Reyles 6785', 'localidad':' Durazno'},
{'nombre':'  Durazno Este'  , 'departamento':'Durazno', 'direccion':  'Los abetos 5678', 'localidad':' Sarandi del Yi'},
{'nombre':'  Artigas Central' , 'departamento':'Artigas', 'direccion':  'Manuel Lavalleja 3456', 'localidad':' Artigas'},
{'nombre':'  Artigas Norte' , 'departamento':'Artigas', 'direccion':  'Brandzen 6789', 'localidad':' Bella Union'},
]




# ===============================
# Carga Usuarios a la base de datos =
# ===============================
# Se ejecutan cuando cuando se accede a la ruta 'localhost/carga_usuarios/'
# al ejecutar esta funcion se cargan registros a la tabla Usuarios
def carga_usuarios(request):

    ROLES = ['usuario', 'farmacia', 'medico', 'stock']

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

    print("paso por la funcion carga_usuaros")

    return redirect('lista_de_usuarios')


USUARIOS = [
    {
        "cedula_de_identidad": 26576383,
        "rol": 0,
        "usuario": "Rowe872",
        "nombre": "Santiago",
        "apellido": "Collins",
        "fecha_de_nacimiento": "2009-11-05",
        "email": "santiagocollins@parcoe.com",
        "telefono": 94247985,
        "direccion": "384 Randolph Street, Eagletown, Utah, 8901"
    },
    {
        "cedula_de_identidad": 40239210,
        "rol": 3,
        "usuario": "Hendricks755",
        "nombre": "Allyson",
        "apellido": "Page",
        "fecha_de_nacimiento": "1986-05-31",
        "email": "allysonpage@parcoe.com",
        "telefono": 98724006,
        "direccion": "707 Grand Street, Chaparrito, Illinois, 1491"
    },
    {
        "cedula_de_identidad": 17147749,
        "rol": 0,
        "usuario": "Jana588",
        "nombre": "Earline",
        "apellido": "Blake",
        "fecha_de_nacimiento": "1954-10-28",
        "email": "earlineblake@parcoe.com",
        "telefono": 91756343,
        "direccion": "603 Empire Boulevard, Harleigh, Virginia, 6529"
    },
    {
        "cedula_de_identidad": 48479504,
        "rol": 1,
        "usuario": "Trisha959",
        "nombre": "Gonzalez",
        "apellido": "Grant",
        "fecha_de_nacimiento": "1962-08-20",
        "email": "gonzalezgrant@parcoe.com",
        "telefono": 95241940,
        "direccion": "471 Seacoast Terrace, Thermal, Texas, 3270"
    },
    {
        "cedula_de_identidad": 64955168,
        "rol": 3,
        "usuario": "Huffman372",
        "nombre": "Powell",
        "apellido": "Cantu",
        "fecha_de_nacimiento": "1999-02-03",
        "email": "powellcantu@parcoe.com",
        "telefono": 98787305,
        "direccion": "292 Ocean Court, Sanborn, Wyoming, 8173"
    },
    {
        "cedula_de_identidad": 49146380,
        "rol": 3,
        "usuario": "Fry372",
        "nombre": "Josephine",
        "apellido": "Golden",
        "fecha_de_nacimiento": "1943-04-19",
        "email": "josephinegolden@parcoe.com",
        "telefono": 94446924,
        "direccion": "552 Kane Street, Bluetown, Wisconsin, 3658"
    },
    {
        "cedula_de_identidad": 32155540,
        "rol": 0,
        "usuario": "Parker135",
        "nombre": "Davis",
        "apellido": "Hubbard",
        "fecha_de_nacimiento": "1987-07-22",
        "email": "davishubbard@parcoe.com",
        "telefono": 94969596,
        "direccion": "875 Greene Avenue, Hinsdale, New Jersey, 4548"
    },
    {
        "cedula_de_identidad": 38982891,
        "rol": 2,
        "usuario": "Hall876",
        "nombre": "Spencer",
        "apellido": "Cantrell",
        "fecha_de_nacimiento": "1999-09-03",
        "email": "spencercantrell@parcoe.com",
        "telefono": 94804275,
        "direccion": "191 Canal Avenue, Nipinnawasee, Oklahoma, 4793"
    },
    {
        "cedula_de_identidad": 57343062,
        "rol": 2,
        "usuario": "Kerr728",
        "nombre": "Dee",
        "apellido": "Irwin",
        "fecha_de_nacimiento": "2012-08-01",
        "email": "deeirwin@parcoe.com",
        "telefono": 99766561,
        "direccion": "650 Bancroft Place, Bentley, Arkansas, 4812"
    },
    {
        "cedula_de_identidad": 57939214,
        "rol": 2,
        "usuario": "Perry610",
        "nombre": "Antoinette",
        "apellido": "Mccoy",
        "fecha_de_nacimiento": "1996-07-23",
        "email": "antoinettemccoy@parcoe.com",
        "telefono": 93556987,
        "direccion": "867 Nostrand Avenue, Bradenville, Virgin Islands, 9594"
    },
    {
        "cedula_de_identidad": 18926939,
        "rol": 1,
        "usuario": "Castro455",
        "nombre": "Stanton",
        "apellido": "Robertson",
        "fecha_de_nacimiento": "2010-07-13",
        "email": "stantonrobertson@parcoe.com",
        "telefono": 99447516,
        "direccion": "538 Powers Street, Carlton, Idaho, 3437"
    },
    {
        "cedula_de_identidad": 35254813,
        "rol": 3,
        "usuario": "Hollie326",
        "nombre": "Pauline",
        "apellido": "Farley",
        "fecha_de_nacimiento": "1977-05-06",
        "email": "paulinefarley@parcoe.com",
        "telefono": 91520512,
        "direccion": "756 Crescent Street, Gerton, Colorado, 5700"
    },
    {
        "cedula_de_identidad": 68020846,
        "rol": 0,
        "usuario": "Irwin819",
        "nombre": "Cole",
        "apellido": "Mcintyre",
        "fecha_de_nacimiento": "2018-01-27",
        "email": "colemcintyre@parcoe.com",
        "telefono": 96046115,
        "direccion": "652 Cumberland Walk, Williams, North Dakota, 5967"
    },
    {
        "cedula_de_identidad": 12471780,
        "rol": 3,
        "usuario": "Merle334",
        "nombre": "Shepard",
        "apellido": "Crawford",
        "fecha_de_nacimiento": "2020-10-13",
        "email": "shepardcrawford@parcoe.com",
        "telefono": 95914594,
        "direccion": "100 Wyona Street, Cartwright, Louisiana, 7759"
    },
    {
        "cedula_de_identidad": 45918227,
        "rol": 3,
        "usuario": "Sherry121",
        "nombre": "Downs",
        "apellido": "Kelley",
        "fecha_de_nacimiento": "2004-01-22",
        "email": "downskelley@parcoe.com",
        "telefono": 96866153,
        "direccion": "889 Allen Avenue, Idledale, South Carolina, 2198"
    },
    {
        "cedula_de_identidad": 61380698,
        "rol": 3,
        "usuario": "Maryellen799",
        "nombre": "Langley",
        "apellido": "Stafford",
        "fecha_de_nacimiento": "1956-07-17",
        "email": "langleystafford@parcoe.com",
        "telefono": 97431998,
        "direccion": "617 Dunham Place, Marienthal, Ohio, 850"
    }
]


"""
###################################################################
plantilla para generar los datos en: https://www.json-generator.com/
###################################################################
 [
  '{{repeat(12, 20)}}',
  {
    cedula_de_identidad:'{{integer(10000000, 70000000)}}',
    rol:'{{integer(0, 3)}}',
    usuario: '{{firstName()}}{{integer(100, 999)}}',
    nombre: '{{firstName()}}',
    apellido: '{{surname()}}',
    fecha_de_nacimiento: '{{date(new Date(1940, 0, 1), new Date(), "YYYY-MM-dd")}}',
    email: '{{email()}}',
    telefono: '09{{integer(1000000, 9999999)}}',
    direccion: '{{integer(100, 999)}} {{street()}}, {{city()}}, {{state()}}, {{integer(100, 10000)}}'
  }
]
"""
