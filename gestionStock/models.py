from django.db import models
from django.db.models.base import Model


#import datetime
#from datetime import datetime
#import time
from datetime import date
from django.core.exceptions import ValidationError
#from django import forms

#from gestionUsuarios.models import Usuarios
#from gestionUsuarios.models import Recetas


#==============
# Medicamentos =
#==============
class Medicamentos(models.Model):
        CATEGORIAS_DE_MEDICAMENTOS = [
                ('VL', 'Venta Libre'),
                ('RV','Receta Verde'),
                ('FNR','Fondo Nacional De Recursos')
        ]

        id = models.AutoField(primary_key=True)
        nombre_comercial = models.CharField(max_length=100)
        #categoria = models.CharField(max_length=50, verbose_name='Categoria(venta libre, receta verde o FNR)')
        categoria = models.CharField(max_length=50, choices=CATEGORIAS_DE_MEDICAMENTOS,verbose_name='Categoria(venta libre, receta verde o FNR)',blank=True, null=True)
        laboratorio = models.CharField(max_length=100,blank=True, null=True)
        principio_activo = models.CharField(max_length=200,blank=True, null=True)
        forma = models.CharField(max_length=50, blank=True, null=True)
        contraindicaciones = models.CharField(max_length=1000,blank=True, null=True)

        def __str__(self):
                return self.nombre_comercial + " -> "+ self.principio_activo
        
        class Meta:
                verbose_name = "Medicamento"
                verbose_name_plural = "Medicamentos"
                ordering = ["nombre_comercial"]



#===========
# Farmacias =
#===========
class Farmacias(models.Model):
        id = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=100)
        direccion = models.CharField(max_length=100, blank=True, null=True)
        localidad = models.CharField(max_length=100,blank=True, null=True)
        departamento = models.CharField(max_length=50, blank=True, null=True)
        funcionarios = models.ManyToManyField('gestionUsuarios.Usuarios',blank=True, verbose_name="Funcionarios")

        def __str__(self):
                return self.nombre + ", " + self.localidad + ", " + self.departamento

        def consultar_stock_acumulado(self, id_medicamento):

                stock_acumulado = 0

                lotes = Lotes.objects.filter(ubicacion=self.id).filter(medicamento=id_medicamento)
                for lote in lotes:
                        stock_acumulado += lote.stock


                return stock_acumulado
        
        class Meta:
                verbose_name = "Farmacia"
                verbose_name_plural = "Farmacias"
                ordering = ["nombre"]




#=======
# Lotes =
#=======
class Lotes(models.Model):

        #intento hacer la validacion de las fechas pasadas
        """
        def clean(self):
                today = date.today()
                if self.vencimiento < str(today):
                       raise ValidationError("La fecha de vencimiento no puede ser anterior a hoy!")
                return self.vencimiento
        """

        id = models.AutoField(primary_key=True)
        
        #medicamento (id_medicamento)
        medicamento = models.ForeignKey(Medicamentos, on_delete=models.CASCADE)
        principio_activo = models.CharField(max_length=200,blank=True, null=True)
        #funcionarios = models.ManyToManyField('gestionUsuarios.Usuarios',blank=True, verbose_name="Funcionarios")
        funcionario = models.ForeignKey('gestionUsuarios.Usuarios', on_delete=models.CASCADE,blank=True, null=True, related_name='funcionario')
        stock = models.IntegerField()
        
        #ubicacion (id_farmacia)
        ubicacion = models.ForeignKey(Farmacias, on_delete=models.CASCADE)
        receta_de_destino = models.ForeignKey('gestionUsuarios.Recetas', on_delete=models.CASCADE,blank=True, null=True, related_name='receta_de_destino')
        
        ingreso = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de ingreso",blank=True, null=True)
        vencimiento = models.CharField(max_length = 50,verbose_name="Fecha de vencimiento",blank=True, null=True) #validators=[validate_date])

        #created = models.CharField(verbose_name="Fecha de creación", max_length=100, blank=True, default=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación",blank=True, null=True)
        updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición",blank=True, null=True)

        

        def __str__(self):
                return str(self.stock) + " unidades de " + str(self.medicamento) + " con vencimiento " + str(self.vencimiento)
        
        class Meta:
                verbose_name = "Lote"
                verbose_name_plural = "Lotes"
                ordering = ["stock"]


