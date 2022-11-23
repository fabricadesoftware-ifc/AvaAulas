# Importações login
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from telnetlib import STATUS
# Importações importantes do django
from django.shortcuts import redirect, render,  get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# Aleatorias
from django.utils import timezone

# Funções de login
def cadastro(request):
    status = request.GET.get('status')
    if request.method == "GET":
        return render(request, 'cadastro.html', {'status': status})

    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=username).first()

    if len(senha) < 6:
        return redirect('/auth/cadastro/?status=1')

    if len(username) < 3:
        return redirect('/auth/cadastro/?status=2')

    if user:
        return redirect('/auth/cadastro/?status=3')

    user = User.objects.create_user(
        username=username, email=email, password=senha)
    user.save()

    return redirect('/auth/login/?status=0')


def login(request):
    status = request.GET.get('status')
    if request.method == "GET":
        return render(request, 'login.html', {'status': status})
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login_django(request, user)
            return render(request, 'index.html')
        else:
            return redirect('/auth/login/?status=4')


def sair(request):
    logout(request)
    return HttpResponseRedirect('/auth/login')

# Funções das telas
def plataforma(request):
    return render(request, 'index.html')


