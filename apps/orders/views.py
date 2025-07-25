from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from apps.orders.forms import RegistrationForm, LoginForm
from django.contrib import messages
from .forms import SimplePasswordResetForm


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        login_form = LoginForm()
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('storage_units:my_rent')
    else:
        form = RegistrationForm()
        login_form = LoginForm()

    return render(request, 'index.html', {
        'registration_form': form,
        'login_form': login_form,
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        reg_form = RegistrationForm()
        if form.is_valid():
            login(request, form.get_user())
            return redirect('storage_units:my_rent')
    else:
        form = LoginForm()
        reg_form = RegistrationForm()

    return render(request, 'index.html', {
        'login_form': form,
        'registration_form': reg_form,
    })


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из аккаунта.')
    return redirect('storage_units:index')

def simple_password_reset_view(request):
    if request.method == 'POST':
        form = SimplePasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пароль успешно обновлён.')
        else:
            request.session['reset_form_errors'] = form.errors.as_json()
            request.session['reset_form_data'] = request.POST
        return redirect('storage_units:index')