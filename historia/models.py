from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone  # <--- IMPORTANTE: Necesario para calcular el tiempo
import math

# --- MODELO DE RECUERDOS ---
class Momento(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título del recuerdo")
    descripcion = models.TextField(verbose_name="Carta o Descripción")
    
    foto = CloudinaryField('image', folder='recuerdos', blank=True, null=True)
    video = CloudinaryField('video', resource_type='video', folder='videos', blank=True, null=True)
    
    fecha = models.DateField(verbose_name="Fecha del recuerdo")

    class Meta:
        verbose_name = "Momento"
        verbose_name_plural = "Nuestros Momentos"
        ordering = ['fecha']

    def __str__(self):
        return f"{self.titulo} ({self.fecha})"


# --- MODELO PARA EL GESTOR DE MÚSICA ---
class Cancion(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título de la canción")
    archivo = CloudinaryField('audio', resource_type='video', folder='musica')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Canción"
        verbose_name_plural = "Lista de Música"
        ordering = ['-fecha_subida']

    def __str__(self):
        return self.titulo


# --- MODELO PARA LA LISTA DE DESEOS ---
class Deseo(models.Model):
    texto = models.CharField(max_length=255)
    cumplido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texto


# --- NUEVO MODELO: MASCOTA COMPARTIDA (TIPO POU) ---
class Mascota(models.Model):
    nombre = models.CharField(max_length=50, default="Pochita") # Pueden cambiarle el nombre
    
    # Estadísticas del 0 al 100
    hambre = models.IntegerField(default=100)      # 100 = Llenito
    felicidad = models.IntegerField(default=100)   # 100 = Muy feliz
    energia = models.IntegerField(default=100)     # 100 = Con mucha energía
    higiene = models.IntegerField(default=100)     # 100 = Limpio
    
    # Campo clave: Guarda cuándo fue la última vez que interactuaron
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Nuestra Mascota"

    def calcular_estado_actual(self):
        """
        Calcula cuánto han bajado las estadísticas basándose en el tiempo
        que ha pasado desde 'ultima_actualizacion' hasta 'ahora'.
        """
        ahora = timezone.now()
        diferencia = ahora - self.ultima_actualizacion
        # Convertimos la diferencia a horas (pueden ser decimales, ej: 1.5 horas)
        horas_pasadas = diferencia.total_seconds() / 3600

        # CONFIGURACIÓN DE DIFICULTAD (Puntos que pierde por hora)
        # Puedes ajustar estos números si quieres que el juego sea más difícil o fácil
        desgaste_hambre = 5    # Pierde 5 de hambre por hora
        desgaste_energia = 4   # Pierde 4 de energía por hora
        desgaste_higiene = 3   # Se ensucia 3 puntos por hora
        desgaste_felicidad = 2 # Se pone triste 2 puntos por hora

        if horas_pasadas > 0.05: # Solo actualiza si han pasado al menos 3 minutos
            self.hambre = max(0, self.hambre - int(horas_pasadas * desgaste_hambre))
            self.energia = max(0, self.energia - int(horas_pasadas * desgaste_energia))
            self.higiene = max(0, self.higiene - int(horas_pasadas * desgaste_higiene))
            self.felicidad = max(0, self.felicidad - int(horas_pasadas * desgaste_felicidad))
            
            # Guardamos los nuevos valores. 
            # OJO: save() actualiza 'ultima_actualizacion' automáticamente por el auto_now=True
            self.save()

    def __str__(self):
        return f"{self.nombre} (Hambre: {self.hambre}%)"