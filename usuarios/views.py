from calendar import c
import email
from django.utils import timezone
from http.client import HTTPResponse
from django.shortcuts import render,  get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect 
from django.urls import reverse
from django.views import generic
from .models import Pergunta, Opcao

def cadastro(request):
    if request.method == "GET":
      return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email= request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse("Ja tem um nego com esse nome boy")

        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        return render(request, 'login.html')

def login(request):
     if request.method == "GET":
         return render(request, 'login.html')
     else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:  
            login_django(request, user)
            return render(request, 'index.html')
        else: 
            return HttpResponse("email ou senha invalidos") 

def plataforma(request):
     return render(request, 'index.html')


def sair(request):
    logout(request)
    return HttpResponseRedirect('/auth/login')



class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'lista_ultimas_perguntas'
    def get_queryset(self):
        return Pergunta.objects.filter(
        data_publicacao__lte=timezone.now()
        ).order_by('-data_publicacao')[:5]
        

class DetalheView(generic.DetailView):

    model = Pergunta
    template_name = 'detalhe.html'


class ResultadosView(generic.DetailView):
    model = Pergunta
    template_name = 'resultados.html'
    

def voto(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    try:
        opcao_selecionada = pergunta.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'detalhe.html', {
            'pergunta': pergunta,
            'error_message': "Você não selecionou uma opção.",
        })
    else:
        opcao_selecionada.votos += 1
        opcao_selecionada.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('resultados', args=(pergunta_id,)))
