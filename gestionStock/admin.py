from django.contrib import admin

# Register your models here.
from gestionStock.models import Medicamentos, Lotes, Farmacias


#la siguiente clase se declara para poder manipular la tabla desde el panel de administrador
class FarmaciasAdmin(admin.ModelAdmin):
        # asi se determinan las columnas que muestra el panel admin
        list_display=("nombre", "localidad", "departamento")

        # aca se determinan los criterios de busqueda que admite el buscador
        search_fields=("nombre", "localidad", "departamento")


class MedicamentosAdmin(admin.ModelAdmin):
        # asi se determinan los filtros que se le pueden aplicar a la derecha de los registros
        list_filter=("categoria",)
        #columnas que se muestran
        list_display=("id","nombre_comercial","principio_activo")

class LotesAdmin(admin.ModelAdmin):
        #columnas que se muestran
        list_display=("id","medicamento","principio_activo", "stock", "ubicacion", "receta_de_destino", "ingreso", "vencimiento", "created", "updated" )
        
        # asi se determinan los filtros que se le pueden aplicar a la derecha de los registros
        list_filter=("vencimiento",)
        
        #filtro tipo migas de pan
        #date_hierarchy="vencimiento"




# con las siguientes lineas declaramos que tablas queremos administrar desde el panel de administracion
admin.site.register(Medicamentos, MedicamentosAdmin)
admin.site.register(Lotes,LotesAdmin)
admin.site.register(Farmacias, FarmaciasAdmin)

