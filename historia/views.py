from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt # <--- IMPORTANTE: Necesario para el juego
import json

# IMPORTANTE: Agregamos 'Mascota' a la lista
from .models import Momento, Cancion, Deseo, Mascota 
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


# --- VISTAS DEL GESTOR DE MÚSICA ---

def lista_canciones(request):
    """Devuelve la lista de canciones, incluyendo la predeterminada manualmente"""
    canciones_data = []
    
    # 1. Agregamos la canción predeterminada manualmente al principio
    canciones_data.append({
        'id': 0, 
        'titulo': 'Canción Predeterminada (Nuestra Canción)',
        'archivo': '/media/cancion.mp3', 
        'es_default': True 
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


# --- VISTAS PARA LA LISTA DE DESEOS ---

def api_deseos(request):
    """Obtiene todos los deseos o crea uno nuevo"""
    if request.method == 'GET':
        # Ordenamos: primero los NO cumplidos (False), luego por fecha
        deseos = Deseo.objects.all().order_by('cumplido', '-fecha_creacion')
        data = [{"id": d.id, "texto": d.texto, "done": d.cumplido} for d in deseos]
        return JsonResponse(data, safe=False)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            texto = data.get('texto')
            if texto:
                deseo = Deseo.objects.create(texto=texto)
                return JsonResponse({'status': 'ok', 'id': deseo.id, 'texto': deseo.texto})
        except:
            return JsonResponse({'status': 'error'}, status=400)
    
    return JsonResponse({'status': 'error'}, status=400)

@require_POST
def api_alternar_deseo(request, id):
    """Marca un deseo como cumplido o pendiente"""
    deseo = get_object_or_404(Deseo, id=id)
    deseo.cumplido = not deseo.cumplido 
    deseo.save()
    return JsonResponse({'status': 'ok', 'done': deseo.cumplido})

@require_POST
def api_eliminar_deseo(request, id):
    """Borra un deseo de la base de datos"""
    deseo = get_object_or_404(Deseo, id=id)
    deseo.delete()
    return JsonResponse({'status': 'ok'})

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt 
import json

# Tus modelos
from .models import Momento, Cancion, Deseo, Mascota 
from .forms import MomentoForm, CancionForm

# --- (AQUÍ VAN TUS VISTAS DE MOMENTOS, MÚSICA Y DESEOS IGUAL QUE ANTES) ---
# ... (He omitido esa parte para no hacer esto larguísimo, déjala como estaba) ...


# ==========================================
# --- VISTA DE LA MASCOTA (ACTUALIZADA) ---
# ==========================================

@csrf_exempt
def api_mascota(request):
    """
    Maneja el estado de la mascota compartida.
    """
    # Usamos ID=1 para la mascota compartida
    pet, created = Mascota.objects.get_or_create(id=1)

    if request.method == 'GET':
        pet.calcular_estado_actual()
        return JsonResponse({
            "nombre": pet.nombre,
            "hambre": pet.hambre,
            "felicidad": pet.felicidad,
            "energia": pet.energia,
            "higiene": pet.higiene
        })

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            accion = data.get('accion')

            # --- LÓGICA DEL JUEGO ---

            if accion == 'comer':
                pet.hambre = min(100, pet.hambre + 20) 
                pet.energia = min(100, pet.energia + 5) 
                pet.higiene = max(0, pet.higiene - 5) # Comer ensucia un poquito

            elif accion == 'jugar':
                pet.felicidad = min(100, pet.felicidad + 15)
                pet.energia = max(0, pet.energia - 10) 
                pet.higiene = max(0, pet.higiene - 10) # Jugar ensucia más

            elif accion == 'dormir':
                pet.energia = 100 # Recarga total
                pet.hambre = max(0, pet.hambre - 15) # Despierta con hambre

            # --- AQUÍ ESTÁ EL CAMBIO IMPORTANTE ---
            elif accion == 'limpiar': 
                pet.higiene = 100 # ¡Queda brillante!
                pet.felicidad = min(100, pet.felicidad + 10) # Le gusta estar limpia
            # --------------------------------------

            pet.save()
            
            return JsonResponse({
                "status": "ok", 
                "hambre": pet.hambre,
                "felicidad": pet.felicidad,
                "energia": pet.energia,
                "higiene": pet.higiene
            })
        except Exception as e:
            print(f"Error en mascota: {e}")
            return JsonResponse({'status': 'error'}, status=400)
            
    return JsonResponse({'status': 'error'}, status=405)