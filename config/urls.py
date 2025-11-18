from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from historia.views import index, eliminar_momento, editar_momento # <--- AGREGAMOS ESTO

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('eliminar/<int:momento_id>/', eliminar_momento, name='eliminar'), # <--- NUEVA RUTA
    path('editar/<int:momento_id>/', editar_momento, name='editar'),       # <--- NUEVA RUTA
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)