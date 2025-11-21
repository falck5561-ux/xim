from django.db import models
from cloudinary.models import CloudinaryField  # <--- IMPORTANTE: Importar esto

# --- MODELO DE RECUERDOS ---
class Momento(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título del recuerdo")
    descripcion = models.TextField(verbose_name="Carta o Descripción")
    
    # CORRECCIÓN 1: Usar CloudinaryField para la foto
    foto = CloudinaryField('image', folder='recuerdos', blank=True, null=True)
    
    # CORRECCIÓN 2: Usar CloudinaryField para el video
    # resource_type='video' es OBLIGATORIO para videos
    video = CloudinaryField('video', resource_type='video', folder='videos', blank=True, null=True)
    
    fecha = models.DateField(verbose_name="Fecha del recuerdo")

    class Meta:
        verbose_name = "Momento"
        verbose_name_plural = "Nuestros Momentos"
        ordering = ['fecha']

    def __str__(self):
        return f"{self.titulo} ({self.fecha})"


# --- NUEVO MODELO PARA EL GESTOR DE MÚSICA ---
class Cancion(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título de la canción")
    
    # CORRECCIÓN 3: La música también se trata como 'video' (audio/video) en Cloudinary
    archivo = CloudinaryField('audio', resource_type='video', folder='musica')
    
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Canción"
        verbose_name_plural = "Lista de Música"
        ordering = ['-fecha_subida']

    def __str__(self):
        return self.titulo