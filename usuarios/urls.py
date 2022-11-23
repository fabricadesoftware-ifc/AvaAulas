from django.urls import path, include
from . import views

urlpatterns = [
    path('cadastro/',views.cadastro, name ='cadastro'),
    path('login/',views.login, name ='login'),
    path('sair/', views.sair, name='sair'),
    path('', views.plataforma, name='plataforma'),
]