from django.db import models
from django.contrib.auth.models import User # Para el usuario que sube el libro

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    genero = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_publicacion = models.DateField(blank=True, null=True)
    portada = models.ImageField(upload_to='portadas/', blank=True, null=True)
    documento_pdf = models.FileField(upload_to='libros_pdf/', blank=True, null=True)
    usuario_carga = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    es_publico = models.BooleanField(default=True) # Para control de acceso

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.usuario.username} en {self.libro.titulo}'