from django.urls import path, include
from . import views

urlpatterns = [
    path('cadastro/',views.cadastro, name ='cadastro'),
    path('login/',views.login, name ='login'),
    path('sair/', views.sair, name='sair'),
    path('', views.plataforma, name='plataforma'),
    path('<int:pk>/resultados/', views.ResultadosView.as_view(), name='resultados'),
    path('<int:pergunta_id>/vote/', views.voto, name='voto'),
]