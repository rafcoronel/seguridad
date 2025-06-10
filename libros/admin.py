from django.contrib import admin
from .models import Libro, Comentario # Importa tus modelos

# Puedes personalizar cómo se muestran los modelos en el admin
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'genero', 'usuario_carga', 'fecha_carga', 'es_publico')
    list_filter = ('genero', 'es_publico', 'fecha_carga')
    search_fields = ('titulo', 'autor', 'isbn', 'descripcion')
    date_hierarchy = 'fecha_carga' # Agrega un navegador de fechas
    ordering = ('-fecha_carga',) # Ordenar por fecha de carga descendente

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('libro', 'usuario', 'fecha_creacion', 'texto')
    list_filter = ('libro', 'usuario', 'fecha_creacion')
    search_fields = ('texto',)

# Registra tus modelos con las opciones de administración personalizadas
admin.site.register(Libro, LibroAdmin)
admin.site.register(Comentario, ComentarioAdmin)