from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('usuarios.urls')),
    path('inicio/', include('plataforma.urls')),
    path('aulas/', include('plataforma.urls')),
    path('resultados/', include('resultados.urls')),
    path('', include('usuarios.urls')),
    path('', include('plataforma.urls'))
]
