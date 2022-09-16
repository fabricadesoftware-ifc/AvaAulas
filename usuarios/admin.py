from django.contrib import admin

from .models import Pergunta, Opcao

class OpcaoInline(admin.StackedInline):
    model = Opcao
    extra = 0

class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('pergunta_texto', 'data_publicacao','publicado_recentemente')
    list_filter = ['data_publicacao']
    search_fields = ['pergunta_texto']
    inlines = [OpcaoInline]
