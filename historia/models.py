from django.db import models

class Momento(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título del recuerdo")
    descripcion = models.TextField(verbose_name="Carta o Descripción")
    
    # Ahora la foto es opcional (blank=True)
    foto = models.ImageField(upload_to='recuerdos/', verbose_name="Foto", blank=True, null=True)
    
    # Nuevo campo para Video
    video = models.FileField(upload_to='videos/', verbose_name="Video (Opcional)", blank=True, null=True)
    
    fecha = models.DateField(verbose_name="Fecha del recuerdo")

    class Meta:
        verbose_name = "Momento"
        verbose_name_plural = "Nuestros Momentos"
        ordering = ['fecha']

    def __str__(self):
        return f"{self.titulo} ({self.fecha})"