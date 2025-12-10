from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from historia import views  # Importamos el archivo de vistas completo

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- RUTAS PRINCIPALES ---
    path('', views.index, name='home'),
    path('eliminar/<int:momento_id>/', views.eliminar_momento, name='eliminar'),
    path('editar/<int:momento_id>/', views.editar_momento, name='editar'),
    
    # --- RUTAS DE LA API DE MÚSICA ---
    path('api/canciones/', views.lista_canciones, name='lista_canciones'),
    path('api/subir-cancion/', views.subir_cancion, name='subir_cancion'),
    path('api/eliminar-cancion/<int:cancion_id>/', views.eliminar_cancion, name='eliminar_cancion'),
    path('api/renombrar-cancion/<int:cancion_id>/', views.renombrar_cancion, name='renombrar_cancion'),

    # --- RUTAS PARA LISTA DE DESEOS ---
    path('api/deseos/', views.api_deseos, name='api_deseos'),
    path('api/deseos/alternar/<int:id>/', views.api_alternar_deseo, name='api_alternar_deseo'),
    path('api/deseos/eliminar/<int:id>/', views.api_eliminar_deseo, name='api_eliminar_deseo'),

    # --- NUEVA RUTA PARA LA MASCOTA (POU) ---
    path('api/mascota/', views.api_mascota, name='api_mascota'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)