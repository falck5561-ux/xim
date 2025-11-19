from django.db import models

# --- MODELO DE RECUERDOS (Ya lo tenías) ---
class Momento(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título del recuerdo")
    descripcion = models.TextField(verbose_name="Carta o Descripción")
    
    # Foto opcional
    foto = models.ImageField(upload_to='recuerdos/', verbose_name="Foto", blank=True, null=True)
    
    # Video opcional
    video = models.FileField(upload_to='videos/', verbose_name="Video (Opcional)", blank=True, null=True)
    
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
    archivo = models.FileField(upload_to='musica/', verbose_name="Archivo de Audio")
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Canción"
        verbose_name_plural = "Lista de Música"
        ordering = ['-fecha_subida']

    def __str__(self):
        return self.titulo