from django import forms
from .models import Momento

class MomentoForm(forms.ModelForm):
    class Meta:
        model = Momento
        fields = ['titulo', 'descripcion', 'fecha', 'foto', 'video'] # <--- Agregamos video aquí
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Nuestro concierto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}), # <--- Y aquí
        }