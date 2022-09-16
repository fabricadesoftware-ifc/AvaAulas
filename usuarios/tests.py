# Create your tests here.

import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Pergunta


class PerguntaModelTests(TestCase):

    def teste_publicado_recentemente_com_pergunta_futura(self):
    
        time = timezone.now() + datetime.timedelta(days=30)
        pergunta_futura = Pergunta(data_publicacao=time)
        self.assertIs(pergunta_futura.publicado_recentemente(), False)
    
    def teste_publicado_recentemente_com_pergunta_antiga(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        pergunta_antiga = Pergunta(data_publicacao=time)
        self.assertIs(pergunta_antiga.publicado_recentemente(), False)

    def teste_publicado_recentemente_com_pergunta_recente(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        pergunta_recente = Pergunta(data_publicacao=time)
        self.assertIs(pergunta_recente.publicado_recentemente(), True)

def criar_pergunta(pergunta_texto, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Pergunta.objects.create(pergunta_texto=pergunta_texto, data_publicacao=time)


class PerguntaIndexViewTests(TestCase):
    def teste_sem_perguntas(self):
       
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sem votação disponível.")
        self.assertQuerysetEqual(response.context['lista_ultimas_perguntas'], [])

    def teste_perguntas_passadas(self):

        criar_pergunta(pergunta_texto="Pergunta Passada.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['lista_ultimas_perguntas'],
            ['<Pergunta: Pergunta Passada.>']
        )

    def teste_perguntas_futuras(self):
       
        criar_pergunta(pergunta_texto="Pergunta Futura.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "Sem votação disponível.")
        self.assertQuerysetEqual(response.context['lista_ultimas_perguntas'], [])

    def teste_perguntas_futuras_e_perguntas_passada(self):
        
        criar_pergunta(pergunta_texto="Pergunta Passada.", days=-30)
        criar_pergunta(pergunta_texto="Pergunta Futura.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['lista_ultimas_perguntas'],
            ['<Pergunta: Pergunta Passada.>']
        )

    def teste_duas_perguntas_passadas(self):
        criar_pergunta(pergunta_texto="Pergunta Passada 1.", days=-30)
        criar_pergunta(pergunta_texto="Pergunta Passada 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['lista_ultimas_perguntas'],
            ['<Pergunta: Pergunta Passada 2.>', '<Pergunta: Pergunta Passada 1.>']
        )