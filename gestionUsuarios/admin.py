from django.contrib import admin

# Register your models here.
from gestionUsuarios.models import Roles, Usuarios, Recetas


#la siguiente clase se declara para poder manipular la tabla desde el panel de administrador

class RolesAdmin(admin.ModelAdmin):
        # asi se determinan los filtros que se le pueden aplicar a la derecha de los registros
        list_filter=("nombre",)
        list_display=("id","nombre", "descripcion")


class UsuariosAdmin(admin.ModelAdmin):
        #columnas que se muestran
        list_display=("rol","nombre", "apellido", "usuario", "usuario_activo", "usuario_administrador")
        
        # asi se determinan los filtros que se le pueden aplicar a la derecha de los registros
        list_filter=("rol",)
        
        #filtro tipo migas de pan
        #date_hierarchy="fecha_de_nacimiento"


class RecetasAdmin(admin.ModelAdmin):
        # asi se determinan las columnas que muestra el panel admin
        list_display=("principio_activo", "medico", "paciente", "estado")

        # aca se determinan los criterios de busqueda que admite el buscador
        search_fields=("principio_activo", "paciente", "medico")






# con las siguientes lineas declaramos que tablas queremos administrar desde el panel de administracion
admin.site.register(Roles, RolesAdmin)
admin.site.register(Usuarios,UsuariosAdmin)
admin.site.register(Recetas, RecetasAdmin)

