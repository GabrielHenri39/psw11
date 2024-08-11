from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .ultis import password_is_valid
from django.contrib import auth
from django.urls import reverse
from django.db.transaction import atomic
from django.contrib import messages
from django.contrib.messages import constants
from django.db import DatabaseError


# Create your views here.

def cadastro(request):
    if request.method == "GET":

        if request.user.is_authenticated:
            return redirect(reverse('cadastrar_empresa'))
        return render(request, 'cadastro.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        if not password_is_valid(request, senha, confirmar_senha):
            return redirect(reverse('cadastro'))
        with atomic():
            try:
                if username.strip():
                    messages.add_message(
                        request, constants.ERROR, 'Usuário não pode ficar em branco')
                user, created = User.objects.get_or_create(
                    username=username, password=senha)
                if not created:

                    messages.add_message(
                        request, constants.ERROR, 'Usuário já existe')
                    return redirect(reverse('cadastro'))
                user.save()
                messages.add_message(
                    request, constants.SUCCESS, 'Usuário cadastro  com sucesso')
                return redirect(reverse('login'))

            except DatabaseError as e:
                messages.add_message(
                    request, constants.ERROR, 'Ocorreu um erro durante o cadastro. Tente novamente.')

                return redirect(reverse('cadastro'))


def login(request):
    if request.method == "GET":
        
        if request.user.is_authenticated:
            return redirect(reverse('cadastrar_empresa'))
        return render(request, 'login.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        try:
            user = auth.authenticate(
                request, username=username, password=senha)
            if not user:
                messages.add_message(
                    request, constants.ERROR, 'Usuário ou senha inválidos')
                return redirect(reverse('login'))
            auth.login(request, user)

            return redirect(reverse('cadastrar_empresa'))
        except Exception as e:
            messages.add_message(request, constants.ERROR, 'Ocorreu um erro durante o login. Tente novamente.')

def logout(request):

    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    auth.logout(request)

    return redirect(reverse('login'))
