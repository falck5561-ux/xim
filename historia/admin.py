from django.contrib import admin
from .models import Momento

# Esto hace que la tabla aparezca en el panel de administración
admin.site.register(Momento)