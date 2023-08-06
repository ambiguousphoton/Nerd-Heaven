from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Island, Topic
from .forms import Island_Form
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = user_name)
        except:
            messages.error(request, 'The username is not registered.')

        user  = authenticate(request, username = user_name, password = password)
        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'The password is wrong.')
    context = {'page': page} 
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    page = 'register'
    return render(request, 'base/login_register.html', )

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    islands = Island.objects.filter(Q(topic__name__icontains = q) |
                                    Q(name__icontains = q) |
                                    Q(discription__icontains = q)
                                    ) 
    topics = Topic.objects.all()
    island_count = islands.count()
    context =  {'islands' : islands, 'topics': topics, 'island_count':island_count}
    return render(request, 'Base/Home_Page.html', context)

def island(request, pk):
    island = Island.objects.get(id = pk)
    context = {'island':island}
    return render(request, 'Base/Island.html', context )

@login_required(login_url = '/login')
def create_island(request):
    form = Island_Form

    if request.method == 'POST':
        form = Island_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': Island_Form}
    return render(request, 'Base/island_form.html', context)

@login_required(login_url = '/login')
def update_island(request, pk):
    island = Island.objects.get(id = pk)
    form = Island_Form(instance = island)

    if request.user != island.host:
        return HttpResponse("you are not allow")

    if request.method == 'POST':
        form = Island_Form(request.POST, instance = island)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/island_form.html', context)

@login_required(login_url = '/login')
def delete_island(request, pk):
    island = Island.objects.get(id=pk)

    if request.user != island.host:
        return HttpResponse("you are not allow")

    if request.method == "POST":
        island.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':island})