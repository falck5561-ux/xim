from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai
import os
import random 

# TUS MODELOS
from .models import Momento, Cancion, Deseo, Mascota
from .forms import MomentoForm, CancionForm

# ==========================================
#  CONFIGURACIÓN DE IA (GEMINI)
# ==========================================

API_KEY = "AIzaSyAFKkY4AUfkbpT1QAdKNrxfTeTGhsjmdR4" 
genai.configure(api_key=API_KEY)

# ==========================================
#  VISTA CEREBRO DE POCHITA (MODO HÁMSTER 🐹)
# ==========================================

@csrf_exempt
def cerebro_pochita(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # 1. RECIBIR DATOS
            mensaje_usuario = data.get('mensaje', '')
            accion = data.get('accion', '')
            stats = data.get('stats', {})

            # 2. DEFINIR LA PERSONALIDAD (PROMPT CORREGIDO)
            # AQUI LE DECIMOS QUE ES UN HÁMSTER Y CAMBIAMOS LOS EMOJIS
            prompt = f"""
            Actúa como Pochita, un HÁMSTER adorable, pequeño y esponjoso.
            Tu dueña es "Mami Ximena" y tu creador es "Papi Josue".
            
            ESTADO ACTUAL:
            - Hambre: {stats.get('hambre')}% 
            - Felicidad: {stats.get('felicidad')}%
            
            REGLAS ESTRICTAS:
            1. Si te preguntan matemáticas, responde SOLO el resultado y un emoji (ej: "Son 4 mami 🤓").
            2. Si Ximena está triste, dile que Josue la ama mucho.
            3. Responde MUY CORTO (máximo 1 o 2 frases).
            4. USA SOLO EMOJIS DE HÁMSTER Y COSAS LINDAS (🐹, 🌻, 🥜, 🧀, 🧡, ✨). ¡NO USES EMOJIS DE PERRO!
            5. Menciona cosas de hámster: tus cachetes, tu rueda, semillas de girasol o dormir hecho bolita.
            
            Lo que dijo Ximena: "{mensaje_usuario}"
            Acción que hizo: "{accion}"
            """

            # 3. INTENTAR CONECTAR CON GOOGLE GEMINI
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            frase_final = response.text.strip().replace('"', '').replace('*', '')

        except Exception as e:
            # 🚨 RESPALDO SI FALLA GOOGLE
            print(f"⚠️ Usando frase de respaldo: {e}")
            
            frases_respaldo = [
                "Mami, mis cachetes están llenos de amor... dame un momento 🐹❤️",
                "Estoy corriendo en mi rueda mental... espera tantito 🎡",
                "Mami, se me cayó mi semilla de girasol... ¿qué decías? 🌻",
                "Mi cerebro de hámster necesita una siesta 😴 (Intenta en 30 seg)",
                "¡Squeak squeak! (Significa que te amo, pero espérame tantito) 🧀",
                "Mami, estoy escondiendo comida en mi casita, ya vuelvo 🥜"
            ]
            frase_final = random.choice(frases_respaldo)

        return JsonResponse({'frase': frase_final})

    return JsonResponse({'error': 'Solo POST permitido'}, status=405)


# ==========================================
#  RESTO DE TUS VISTAS (IGUAL QUE SIEMPRE)
# ==========================================

def index(request):
    if request.method == 'POST':
        form = MomentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MomentoForm()
    momentos = Momento.objects.all().order_by('fecha') 
    context = {'momentos': momentos, 'form': form}
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

def lista_canciones(request):
    canciones_data = [{'id': 0, 'titulo': 'Canción Predeterminada', 'archivo': '/media/cancion.mp3', 'es_default': True }]
    for cancion in Cancion.objects.all().order_by('-fecha_subida'):
        if cancion.archivo:
            canciones_data.append({'id': cancion.id, 'titulo': cancion.titulo, 'archivo': cancion.archivo.url, 'es_default': False})
    return JsonResponse({'canciones': canciones_data})

def subir_cancion(request):
    if request.method == 'POST':
        form = CancionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

@require_POST
def eliminar_cancion(request, cancion_id):
    cancion = get_object_or_404(Cancion, id=cancion_id)
    cancion.delete()
    return JsonResponse({'status': 'ok'})

@require_POST
def renombrar_cancion(request, cancion_id):
    try:
        cancion = get_object_or_404(Cancion, id=cancion_id)
        data = json.loads(request.body)
        if data.get('titulo'):
            cancion.titulo = data.get('titulo')
            cancion.save()
            return JsonResponse({'status': 'ok'})
    except: pass
    return JsonResponse({'status': 'error'}, status=400)

def api_deseos(request):
    if request.method == 'GET':
        deseos = Deseo.objects.all().order_by('cumplido', '-fecha_creacion')
        data = [{"id": d.id, "texto": d.texto, "done": d.cumplido} for d in deseos]
        return JsonResponse(data, safe=False)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if data.get('texto'):
                Deseo.objects.create(texto=data.get('texto'))
                return JsonResponse({'status': 'ok'})
        except: pass
    return JsonResponse({'status': 'error'}, status=400)

@require_POST
def api_alternar_deseo(request, id):
    d = get_object_or_404(Deseo, id=id)
    d.cumplido = not d.cumplido 
    d.save()
    return JsonResponse({'status': 'ok', 'done': d.cumplido})

@require_POST
def api_eliminar_deseo(request, id):
    d = get_object_or_404(Deseo, id=id)
    d.delete()
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def api_mascota(request):
    pet, _ = Mascota.objects.get_or_create(id=1)
    if hasattr(pet, 'calcular_estado_actual'):
        pet.calcular_estado_actual() 
    
    if request.method == 'GET':
        return JsonResponse({"hambre": pet.hambre, "felicidad": pet.felicidad, "energia": pet.energia, "higiene": pet.higiene})

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            accion = data.get('accion')
            if accion == 'comer':
                pet.hambre = min(100, pet.hambre + 25)
                pet.energia = min(100, pet.energia + 5)
            elif accion == 'jugar':
                pet.felicidad = min(100, pet.felicidad + 20)
                pet.energia = max(0, pet.energia - 15)
            elif accion == 'dormir':
                pet.energia = 100
            elif accion == 'bañar':
                pet.higiene = 100
            pet.save()
            return JsonResponse({"status": "ok", "hambre": pet.hambre, "felicidad": pet.felicidad, "energia": pet.energia, "higiene": pet.higiene})
        except: pass
    return JsonResponse({'status': 'error'}, status=400)