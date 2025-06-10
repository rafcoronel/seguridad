from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Mixins para seguridad y autenticación
from .models import Libro, Comentario
from .forms import LibroForm, ComentarioForm, CustomUserCreationForm 
import logging # Para el logging de seguridad
from django.views import generic # Importa generic
from django.contrib.auth import login

# Configuración básica de logging para tu aplicación
logger = logging.getLogger('libros') # 'libros' es el nombre del logger que configuraremos en settings.py


# 1. Vista para listar todos los libros (públicos por defecto)
class ListaLibros(ListView):
    model = Libro
    template_name = 'libros/lista_libros.html' # Ruta a tu plantilla HTML
    context_object_name = 'libros' # Nombre de la variable que contendrá la lista de libros en la plantilla
    paginate_by = 10 # Opcional: Para paginación, mostrar 10 libros por página

    def get_queryset(self):
        # Obtiene todos los libros. Si el usuario no está logueado,
        # o si no es staff (administrador), solo muestra los libros 'es_publico=True'.
        # Si es un administrador, puede ver todos los libros (públicos y no públicos).
        if self.request.user.is_authenticated and self.request.user.is_staff:
            logger.info(f"Admin '{self.request.user.username}' viendo todos los libros.")
            return Libro.objects.all()
        logger.info(f"Usuario no autenticado o no-admin viendo libros públicos.")
        return Libro.objects.filter(es_publico=True)

# 2. Vista para ver los detalles de un libro específico y añadir comentarios
class DetalleLibro(DetailView):
    model = Libro
    template_name = 'libros/detalle_libro.html'
    context_object_name = 'libro'

    # Este método se usa para añadir datos extra al contexto que se envía a la plantilla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Asegúrate de que solo los libros públicos sean accesibles si no es un admin
        if not self.object.es_publico and not (self.request.user.is_authenticated and self.request.user.is_staff):
            logger.warning(f"Intento de acceso no autorizado a libro no público: '{self.object.titulo}' por usuario '{self.request.user.username if self.request.user.is_authenticated else 'Anónimo'}'.")
            # Esto es un placeholder. En un caso real, podrías lanzar un 404 o redirigir.
            # Por ahora, simplemente no mostraremos el contenido si no es público.
            return context # Podrías hacer que el template maneje esta condición

        context['comentarios'] = self.object.comentarios.all() # Obtiene todos los comentarios del libro
        context['form_comentario'] = ComentarioForm() # Pasa una instancia vacía del formulario de comentario
        logger.info(f"Mostrando detalle del libro '{self.object.titulo}'.")
        return context

    # Este método maneja las peticiones POST (cuando se envía un formulario)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object() # Obtiene el libro al que se está comentando
        form = ComentarioForm(request.POST) # Crea una instancia del formulario con los datos enviados

        if not request.user.is_authenticated:
            logger.warning(f"Intento de comentar en '{self.object.titulo}' por usuario no autenticado.")
            # Redirige al login si no está autenticado
            return redirect('login') # Asegúrate de que 'login' esté definido en tus URLs

        if form.is_valid():
            comentario = form.save(commit=False) # Crea el objeto Comentario pero no lo guarda en la DB aún
            comentario.libro = self.object # Asigna el libro al comentario
            comentario.usuario = request.user # Asigna el usuario actual al comentario
            comentario.save() # Guarda el comentario en la base de datos
            logger.info(f"Usuario '{request.user.username}' añadió un comentario al libro '{self.object.titulo}'.")
            return redirect('detalle_libro', pk=self.object.pk) # Redirige de vuelta a la página del libro
        else:
            logger.warning(f"Intento fallido de comentar en '{self.object.titulo}' por usuario '{request.user.username}'. Errores: {form.errors.as_json()}")
            # Si el formulario no es válido, vuelve a mostrar la página con los errores
            return self.get(request, *args, **kwargs)

# 3. Vista para crear un nuevo libro
class CrearLibro(LoginRequiredMixin, CreateView): # LoginRequiredMixin asegura que el usuario debe estar logueado
    model = Libro
    form_class = LibroForm # Usa el formulario LibroForm que creamos
    template_name = 'libros/crear_libro.html'
    success_url = reverse_lazy('lista_libros') # A dónde redirigir después de crear el libro

    # Este método se ejecuta antes de guardar el formulario válido
    def form_valid(self, form):
        form.instance.usuario_carga = self.request.user # Asigna automáticamente el usuario actual como cargador
        response = super().form_valid(form) # Llama al método original para guardar el objeto
        logger.info(f"Usuario '{self.request.user.username}' creó el libro '{self.object.titulo}'.")
        return response

    def form_invalid(self, form):
        logger.warning(f"Usuario '{self.request.user.username}' intentó crear un libro con errores. Errores: {form.errors.as_json()}")
        return super().form_invalid(form)

# 4. Vista para actualizar un libro existente
class ActualizarLibro(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libros/actualizar_libro.html' # Necesitarás crear esta plantilla
    success_url = reverse_lazy('lista_libros')

    # UserPassesTestMixin requiere que definas test_func para controlar quién puede acceder
    def test_func(self):
        libro = self.get_object()
        # Solo el usuario que cargó el libro o un superusuario (admin) puede editarlo
        return self.request.user == libro.usuario_carga or self.request.user.is_superuser

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Usuario '{self.request.user.username}' actualizó el libro '{self.object.titulo}'.")
        return response

    def form_invalid(self, form):
        logger.warning(f"Usuario '{self.request.user.username}' intentó actualizar el libro '{self.object.titulo}' con errores. Errores: {form.errors.as_json()}")
        return super().form_invalid(form)


# 5. Vista para eliminar un libro
class EliminarLibro(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Libro
    template_name = 'libros/eliminar_libro.html' # Necesitarás crear esta plantilla
    success_url = reverse_lazy('lista_libros')

    def test_func(self):
        libro = self.get_object()
        # Solo el usuario que cargó el libro o un superusuario (admin) puede eliminarlo
        return self.request.user == libro.usuario_carga or self.request.user.is_superuser

    def form_valid(self, form):
        logger.info(f"Usuario '{self.request.user.username}' eliminó el libro '{self.object.titulo}'.")
        return super().form_valid(form)
    
class RegisterView(generic.CreateView):
    """
    Vista para permitir a los usuarios crear una nueva cuenta.
    Utiliza CustomUserCreationForm para el formulario.
    """
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html' # Ruta a la plantilla HTML de registro
    success_url = reverse_lazy('lista_libros') # Redirige a la página principal después de un registro exitoso

    def form_valid(self, form):
        # Guardar el usuario y luego iniciar sesión al usuario recién registrado
        response = super().form_valid(form)
        login(self.request, self.object) # Inicia sesión al usuario recién creado
        logger.info(f"Nuevo usuario registrado y logueado: '{self.object.username}'.")
        return response

    def form_invalid(self, form):
        logger.warning(f"Intento fallido de registro. Errores: {form.errors.as_json()}")
        return super().form_invalid(form)