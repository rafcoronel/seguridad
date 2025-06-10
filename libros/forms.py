from django import forms
from .models import Libro, Comentario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User # ¡Importa el modelo User!

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'isbn', 'genero', 'descripcion', 'fecha_publicacion', 'portada', 'documento_pdf', 'es_publico']
        # Widgets para mejorar la apariencia de los campos HTML
        widgets = {
            'fecha_publicacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), # Campo de fecha con selector
            'descripcion': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.TextInput(attrs={'class': 'form-control'}),
            # Puedes añadir clases CSS a otros campos si usas un framework como Bootstrap
        }
        labels = { # Puedes personalizar las etiquetas de los campos
            'documento_pdf': 'Archivo PDF del libro (opcional)',
            'es_publico': 'Visible para todos',
        }
        help_texts = { # Los mensajes de ayuda que definiste en models.py se muestran automáticamente
            'isbn': 'Número de identificación estándar de libro (13 dígitos)',
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Añade tu comentario aquí...', 'class': 'form-control'}),
        }
        labels = {
            'texto': 'Tu Comentario',
        }
        
class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para la creación de un nuevo usuario.
    Extiende el UserCreationForm por defecto de Django.
    """
    # Aquí puedes añadir campos adicionales si tuvieras un modelo de usuario personalizado
    # Por ahora, usaremos los campos por defecto de UserCreationForm.

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',) # Agregamos 'email' para que el usuario pueda introducirlo en el registro.
                                                           # Aunque no es obligatorio, es buena práctica.
        labels = {
            'username': 'Nombre de Usuario',
            'password2': 'Confirmar Contraseña',
            'email': 'Correo Electrónico',
        }
        help_texts = {
            'username': 'Obligatorio. De 150 caracteres o menos. Letras, dígitos y @/./+/-/_.',
        }