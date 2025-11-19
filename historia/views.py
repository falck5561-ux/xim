from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST # Importante para seguridad
import json
from .models import Momento, Cancion
from .forms import MomentoForm, CancionForm

# --- VISTAS DE LA HISTORIA (MOMENTOS) ---

def index(request):
    if request.method == 'POST':
        form = MomentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MomentoForm()

    # 'fecha' ordena de la más antigua a la más reciente.
    momentos = Momento.objects.all().order_by('fecha') 
    
    context = {
        'momentos': momentos,
        'form': form
    }
    return render(request, 'index.html', context)

def eliminar_momento(request, momento_id):
    momento = get_object_or_404(Momento, id=momento_id)
    momento.delete()
    return redirect('home')

def editar_momento(request, momento_id):
    momento = get_object_or_404(Momento, id=momento_id)
    if request.method == 'POST':
        form = MomentoForm(request.POST, request.FILES, instance=momento)
        if form.is_valid():
            form.save()
            return redirect('home')
    return redirect('home')


# --- VISTAS DEL GESTOR DE MÚSICA (COMPLETAS) ---

def lista_canciones(request):
    """Devuelve la lista de canciones, incluyendo la predeterminada manualmente"""
    canciones_data = []
    
    # 1. Agregamos la canción predeterminada manualmente al principio
    # Asegúrate de que este archivo exista en tu carpeta media o static
    canciones_data.append({
        'id': 0, # ID especial para identificarla
        'titulo': 'Canción Predeterminada (Nuestra Canción)',
        'archivo': '/media/cancion.mp3', # Ruta fija a tu canción base
        'es_default': True # Marcador para no dejar borrarla en el frontend
    })
    
    # 2. Agregamos las canciones subidas por el usuario
    for cancion in Cancion.objects.all().order_by('-fecha_subida'):
        if cancion.archivo:
            canciones_data.append({
                'id': cancion.id,
                'titulo': cancion.titulo,
                'archivo': cancion.archivo.url,
                'es_default': False
            })
        
    return JsonResponse({'canciones': canciones_data})

def subir_cancion(request):
    """Recibe la canción vía AJAX y la guarda"""
    if request.method == 'POST':
        form = CancionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

@require_POST
def eliminar_cancion(request, cancion_id):
    """Elimina una canción de la base de datos"""
    cancion = get_object_or_404(Cancion, id=cancion_id)
    cancion.delete()
    return JsonResponse({'status': 'ok'})

@require_POST
def renombrar_cancion(request, cancion_id):
    """Cambia el título de una canción"""
    try:
        cancion = get_object_or_404(Cancion, id=cancion_id)
        data = json.loads(request.body)
        nuevo_titulo = data.get('titulo')
        
        if nuevo_titulo:
            cancion.titulo = nuevo_titulo
            cancion.save()
            return JsonResponse({'status': 'ok'})
    except Exception as e:
        print(f"Error al renombrar: {e}")
        pass
        
    return JsonResponse({'status': 'error'}, status=400)