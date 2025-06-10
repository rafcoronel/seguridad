from django.urls import path
from . import views # Importa las vistas de tu aplicación
from django.conf import settings
from django.conf.urls.static import static # Para servir archivos media en desarrollo

urlpatterns = [
    path('', views.ListaLibros.as_view(), name='lista_libros'), # Página principal, lista de libros
    path('libro/<int:pk>/', views.DetalleLibro.as_view(), name='detalle_libro'), # Detalle de un libro (pk es el ID)
    path('libro/crear/', views.CrearLibro.as_view(), name='crear_libro'), # Formulario para crear un libro
    path('libro/<int:pk>/editar/', views.ActualizarLibro.as_view(), name='actualizar_libro'), # Formulario para editar
    path('libro/<int:pk>/eliminar/', views.EliminarLibro.as_view(), name='eliminar_libro'), # Confirmación para eliminar
]

# ¡IMPORTANTE! Esto solo sirve archivos MEDIA (imágenes, PDFs) en modo de desarrollo (DEBUG = True).
# En producción, Nginx o un servicio de almacenamiento en la nube se encargará de esto.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)