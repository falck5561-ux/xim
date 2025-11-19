from django import forms
from .models import Momento, Cancion  # <--- IMPORTANTE: Agregamos Cancion aquí

# --- Formulario para los Recuerdos (Ya lo tenías) ---
class MomentoForm(forms.ModelForm):
    class Meta:
        model = Momento
        fields = ['titulo', 'descripcion', 'fecha', 'foto', 'video']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Nuestro concierto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
        }

# --- NUEVO: Formulario para subir Música ---
class CancionForm(forms.ModelForm):
    class Meta:
        model = Cancion
        fields = ['titulo', 'archivo']
        # No necesitamos widgets complejos aquí porque lo manejamos con AJAX en el frontend