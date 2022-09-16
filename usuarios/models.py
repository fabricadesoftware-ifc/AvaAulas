import datetime
from django.db import models

from django.utils import timezone


class Pergunta(models.Model):
    
    pergunta_texto = models.CharField(max_length=200)
    data_publicacao = models.DateTimeField('Data da Publicação')

    class Meta:
        verbose_name_plural = "Perguntas"
    
    def __str__(self):
        return self.pergunta_texto
    

    def publicado_recentemente(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.data_publicacao <= now
    publicado_recentemente.admin_order_field = 'data_publicacao'
    publicado_recentemente.boolean = True
    publicado_recentemente.short_description = 'Publicado recentemente?'
        


class Opcao(models.Model):
    
    class Meta:
        verbose_name_plural = "Opções"

    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    opcao_texto = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.opcao_texto
