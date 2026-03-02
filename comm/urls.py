from django.urls import path
from . import views

app_name = 'comm'

urlpatterns = [
    path('', views.chat_home, name='home'),
    path('<str:room_name>/', views.chat_room, name='room'),
    path('video/<str:room_name>/', views.video_call, name='video'),
]
