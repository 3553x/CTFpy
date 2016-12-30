from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

def index(request):
    if request.user.is_authenticated:
        return render(request, 'user/index.html', 
                {'base':'base.html', 'user':request.user})
    else:
        return HttpResponseRedirect(reverse('user:register'))

def u_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:index'))
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], 
                    password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect(reverse('user:index'))
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', 
            {'form':form, 'base':'base.html'})


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:index'))
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:login'))
    else:
        form = UserForm()
    return render(request, 'user/register.html', 
            {'form': form, 'base':'base.html'})

def u_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user:index'))

