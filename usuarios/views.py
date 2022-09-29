import http
from itertools import count
from telnetlib import STATUS
from calendar import c
import email
from django.utils import timezone
from http.client import HTTPResponse
from django.shortcuts import render,  get_object_or_404, redirect
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
from .models import Usuario
from hashlib import sha256

def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})

def login(request):
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})
        
def valida_cadastro(request):
    nome = request.POST.get('username')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    usuario = Usuario.objects.filter(email = email)


    if len(senha) < 6:
        return redirect('/auth/cadastro/?status=2')
    
    if len(nome) < 3:
        return redirect('/auth/cadastro/?status=1')

    try:
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome = nome, email = email, senha = senha)
        usuario.save()

        return redirect('/auth/cadastro/?status=0')
    except:
        return HttpResponse("erro5")

def valida_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    senha = sha256(senha.encode()).hexdigest()

    usuario = Usuario.objects.filter(email = email).filter(senha = senha)

    if len(usuario) == 0:
        return redirect('/login/?status=1')
    elif len(usuario) > 0:
        request.session['usuario'] = usuario[0].id
        return redirect (f'/livro/home')

    return redirect('/login/')

def plataforma(request):
     return render(request, 'index.html')


def sair(request):
    logout(request)
    return HttpResponseRedirect('/login')



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
