from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # to restrict the pages
from django.db.models import Q # it helps to provide the funcitonality of or and in our code
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room,Topic
from .forms import RoomForm
# Create your views here.

# rooms = [
#     {'id':1, 'name':'lets learn python'},
#     {'id':2, 'name':'Backend Development'},
#     {'id':3, 'name':'Frontend Development'},
# ]


def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Not Found!')

        user = authenticate(request, username = username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    #search functionality
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        ) 
    # here icontains means case insensitive
    #here objects is a model manager or modle object variable
    #now it is connected to db, we are going to see items from db
    
    topics = Topic.objects.all()
    room_count = rooms.count()
    context ={'rooms':rooms, 'topics': topics, 'room_count':room_count }
    return render(request, 'base/home.html',context)

def room(request,pk):
    # room=None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room=i
    # for being more specific after cliking the bakend develeopment, bakend development must open


    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created') #-created means descending order
    context={'room':room, 'room_messages': room_messages}
    return render(request, 'base/room.html', context)

#decorator: now if the credentials are not matched then the user will be redirected to login page
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        #print(request.POST)
         form = RoomForm(request.POST)
         if form.is_valid():
             form.save()
             return redirect('home') 
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

#for editing the room
@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # so that room value are already filled

    #this will allow only the room owner to edit the room
    if request.user != room.host:
        return HttpResponse('Access Denied!!')


    # processing the data:
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

# Deleting the item
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    #this will allow only the room owner to edit the room
    if request.user != room.host:
        return HttpResponse('Access Denied!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})