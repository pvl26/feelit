from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfileForm
from .models import Profile
import re
import requests

def login_view(request):
    username = request.POST.get('username')
    response = {}
    try:
        user = User.objects.get(username=username)
        login(request, user)
        response["status"] = "success"
    except user.DoesNotExist:
        response["status"] = "fail"
    
    return JsonResponse(response)
    
def logout_view(request):
    logout(request)
    return redirect('homepage')

city = None
def profile(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=d5922c09ab547a2a5de23d7ae5e51f2b'
    global city

    if not city:
        city = "Bucharest"
        
    if request.is_ajax():
        lst = request.POST.getlist('city')
        if lst:
            city = lst[0]

    city_weather = requests.get(url.format(city)).json() 
    weather = {
        'city' : city,
        'temperature' : city_weather['main']['temp'],
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }

    if request.user.is_authenticated:
        return render(request, 'profile.html', context = {
            'weather' : weather
        })
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
                user.profile = Profile()
                login(request, user)
                return redirect('create_profile')
    
    return render(request, 'register.html')
        

def profile_update(request):

    response = {
        "status":"success"
    }
    profile = request.user.profile

    emotions = [
        "happy",
        "hopeful",
        "adventure",
        "chill",
        "dreamy",
        "sad"
    ]
    print(request.POST['current[happy]'])
    for i in range(6):
        value = int(profile.current_moods[emotions[i]])
        value += int(request.POST[f"current[{emotions[i]}]"]) * 10 
        print(int(request.POST[f"current[{emotions[i]}]"]))
        profile.current_moods[emotions[i]] = str(value)
    
    for i in range(6):
        value = int(profile.goal_moods[emotions[i]])
        value += int(request.POST[f"goal[{emotions[i]}]"]) * 10 
        print(int(request.POST[f"goal[{emotions[i]}]"]))
        profile.goal_moods[emotions[i]] = str(value)

    profile.save()
    print(request.POST)


    
    return JsonResponse(response)

def create_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            if profile.user_id is None:
                profile.user_id = request.user.id
                profile.save()
            return render(request, 'profile.html')
    
    else:
        form = ProfileForm()
        print("here")
        return render(request, 'create_profile.html', context={
            'form':form
        })
