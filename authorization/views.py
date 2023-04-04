from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def signup_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        if username != '' and password != '':
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('info_250_coins')
    return render(request, 'registration/signup.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('info_250_coins')
    return render(request, 'registration/login.html')


def logout_page(request):
    logout(request)
    return redirect('welcome_page')
