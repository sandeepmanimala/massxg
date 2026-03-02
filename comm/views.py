from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message

@login_required
def chat_home(request):
    # Get all active rooms, or default rooms
    rooms = ChatRoom.objects.all()
    if not rooms.exists():
        # Auto-create some default biological discussion rooms
        default_rooms = ['General Biology', 'Bioinformatics Setup', 'AI Models', 'Wet Lab Help']
        for name in default_rooms:
            ChatRoom.objects.create(name=name)
        rooms = ChatRoom.objects.all()
    
    return render(request, 'comm/home.html', {'rooms': rooms})

@login_required
def chat_room(request, room_name):
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    # Get the last 50 messages
    messages = room.messages.order_by('-timestamp')[:50]
    messages = reversed(messages) # We want oldest first for display

    return render(request, 'comm/chat.html', {
        'room_name': room_name,
        'messages': messages,
    })

@login_required
def video_call(request, room_name):
    return render(request, 'comm/video.html', {'room_name': room_name})
