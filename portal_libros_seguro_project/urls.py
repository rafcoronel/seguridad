"""
URL configuration for portal_libros_seguro_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importa settings
from django.conf.urls.static import static # Importa static para archivos media
from libros.views import RegisterView # ¡Importa tu vista de registro aquí!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('libros.urls')), # Incluye todas las URLs de tu aplicación 'libros' aquí
    # URLs para autenticación (login, logout, registro de Django)
    path('accounts/', include('django.contrib.auth.urls')), # Django proporciona estas URLs para login, logout, password reset, etc.
    # Puedes añadir tus propias URLs de registro de usuario aquí, si no usas la de admin.
    path('accounts/register/', RegisterView.as_view(), name='register'), # <--- ¡Esta es la nueva URL para el registro!
]

# Configuración para servir archivos media (imágenes, PDFs) en desarrollo
# ¡NO USAR ESTO EN PRODUCCIÓN!
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
