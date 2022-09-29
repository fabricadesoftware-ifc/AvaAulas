from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('cadastro/',views.cadastro, name ='cadastro'),
    path('sair/', views.sair, name='sair'),
    path('', views.plataforma, name='plataforma'),
    path('<int:pk>/resultados/', views.ResultadosView.as_view(), name='resultados'),
    path('<int:pergunta_id>/vote/', views.voto, name='voto'),
    path('valida_cadastro/', views.valida_cadastro, name = 'valida_cadastro'),
    path('valida_login/', views.valida_login, name = 'valida_login'),
]