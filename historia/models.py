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

# --- MODELO MEJORADO: MASCOTA COMPARTIDA ---
class Mascota(models.Model):
    nombre = models.CharField(max_length=50, default="Pochita") 
    
    # Estadísticas del 0 al 100
    hambre = models.IntegerField(default=100)      # 100 = Llenito
    felicidad = models.IntegerField(default=100)   # 100 = Muy feliz
    energia = models.IntegerField(default=100)     # 100 = Con mucha energía
    higiene = models.IntegerField(default=100)     # 100 = Limpio
    
    # Campo clave: Guarda cuándo fue la última vez que se guardó algo
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Nuestra Mascota"

    def calcular_estado_actual(self):
        """
        Calcula el desgaste por tiempo.
        Se ejecuta cada vez que alguien abre la página o toca un botón.
        """
        ahora = timezone.now()
        diferencia = ahora - self.ultima_actualizacion
        horas_pasadas = diferencia.total_seconds() / 3600

        # --- CONFIGURACIÓN DE DIFICULTAD (Balanceada) ---
        # Antes perdía 5/hora (20 horas para morir). 
        # Ahora lo haremos un poco más dinámico:
        desgaste_hambre = 8     # Se vacía en ~12 horas
        desgaste_energia = 6    # Se cansa en ~16 horas
        desgaste_higiene = 5    # Se ensucia en ~20 horas
        desgaste_felicidad = 4  # Se pone triste en ~24 horas

        # Solo actualizamos si ha pasado más de 1 minuto (0.016 horas)
        # para que se sienta "vivo" más rápido.
        if horas_pasadas > 0.01: 
            self.hambre = max(0, self.hambre - int(horas_pasadas * desgaste_hambre))
            self.energia = max(0, self.energia - int(horas_pasadas * desgaste_energia))
            self.higiene = max(0, self.higiene - int(horas_pasadas * desgaste_higiene))
            self.felicidad = max(0, self.felicidad - int(horas_pasadas * desgaste_felicidad))
            
            # Guardamos para actualizar la hora y los nuevos valores
            self.save()

    @property
    def estado_animo(self):
        """Devuelve un texto sobre cómo se siente (Útil para depurar o mostrar)"""
        if self.hambre < 20: return "Hambriento"
        if self.energia < 20: return "Exhausto"
        if self.higiene < 20: return "Sucio"
        if self.felicidad < 20: return "Deprimido"
        return "Feliz"

    def __str__(self):
        return f"{self.nombre} - {self.estado_animo} (H: {self.hambre}%)"