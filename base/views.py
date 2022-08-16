from django.shortcuts import render,redirect
from django.db.models import Q # it helps to provide the funcitonality of or and in our code
from .models import Room,Topic
from .forms import RoomForm
# Create your views here.

# rooms = [
#     {'id':1, 'name':'lets learn python'},
#     {'id':2, 'name':'Backend Development'},
#     {'id':3, 'name':'Frontend Development'},
# ]


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
    context={'room':room}
    return render(request, 'base/room.html', context)

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
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # so that room value are already filled

    # processing the data:
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

# Deleting the item
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})