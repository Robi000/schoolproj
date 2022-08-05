from django.shortcuts import redirect, render
from .forms import my_user_form, UserauthForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import User
# Create your views here.


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'logout_page.html', {})


def register_page(request):
    if request.method == 'POST':
        form = my_user_form(request.POST or None)
        if form.is_valid():
            form.save()
            form = my_user_form()
        else:
            form = my_user_form(request.POST)
    else:
        form = my_user_form()
    context = {
        'form': form,
        'Teachers': User.objects.all()
    }
    return render(request, 'register_page.html', context)


def login_page(request):
    if request.method == 'POST':
        form = UserauthForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserauthForm(request)
    context = {
        'form': form
    }
    return render(request, 'login_page.html', context)
