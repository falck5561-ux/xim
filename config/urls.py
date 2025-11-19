from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# IMPORTAMOS TODAS LAS VISTAS (INCLUYENDO LAS NUEVAS)
from historia.views import (
    index, 
    eliminar_momento, 
    editar_momento, 
    lista_canciones, 
    subir_cancion,
    eliminar_cancion,  # <--- FALTA AGREGAR ESTA
    renombrar_cancion  # <--- Y ESTA
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('eliminar/<int:momento_id>/', eliminar_momento, name='eliminar'),
    path('editar/<int:momento_id>/', editar_momento, name='editar'),
    
    # RUTAS DE LA API DE MÚSICA
    path('api/canciones/', lista_canciones, name='lista_canciones'),
    path('api/subir-cancion/', subir_cancion, name='subir_cancion'),
    
    # --- NUEVAS RUTAS PARA ELIMINAR Y RENOMBRAR ---
    path('api/eliminar-cancion/<int:cancion_id>/', eliminar_cancion, name='eliminar_cancion'),
    path('api/renombrar-cancion/<int:cancion_id>/', renombrar_cancion, name='renombrar_cancion'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)