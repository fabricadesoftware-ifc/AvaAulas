from django.shortcuts import render
from calendar import c
import email
from http.client import HTTPResponse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def plataforma(request):
     return render(request, 'index.html')

@login_required(login_url="/auth/login/")
def aulas(request):
    return render(request, 'aulas.html')
