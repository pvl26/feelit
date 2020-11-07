from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import re

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('pwd')
    response = {}
    try:
        user = User.objects.get(username=username)
        login(request, user)
        response["status"] = "success"
    except User.DoesNotExist:
        response["status"] = "fail"
    
    return JsonResponse(response)
    
def logout_view(request):
    logout(request)
    return redirect('homepage')

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    return redirect('homepage')


def register(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get('username')
        if(username is "" or len(username) > 50):
            return render(request, 'register.html', {'error' : 'Invalid username'})
        password = request.POST.get('password')
        if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            return render(request, 'register.html', {'error' : 'Password must be at least 8 characters'})
        password_conf = request.POST.get('password_conf')
        email = request.POST.get('email')
        try:
            get_user = User.objects.get(email=email)
            return render(request, 'register.html', {'error' : 'Email already used'})
        except User.DoesNotExist:
            try:
                get_user = User.objects.get(username=username)
                return render(request, 'register.html', {'error' : 'Username already used'})
            except User.DoesNotExist:
                if password != password_conf:
                    # password mismatch
                    return render(request, 'register.html', {'error' : 'Password mismatch'})

                user  = User.objects.create(username=username, email=email, password=password)
                login(request, user)
                return render(request, 'homepage.html')
    
    return render(request, 'register.html')
        


