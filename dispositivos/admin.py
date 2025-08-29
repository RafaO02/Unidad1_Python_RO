from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Categoria, Zona, Dispositivo, Medicion

admin.site.register([Categoria, Zona])

admin.site.register(Dispositivo)

admin.site.register(Medicion)