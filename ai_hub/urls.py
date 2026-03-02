from django.urls import path
from . import views

app_name = 'ai_hub'

urlpatterns = [
    path('', views.ai_list, name='list'),
    path('submit/', views.ai_submit, name='submit'),
    path('<int:pk>/', views.ai_detail, name='detail'),
]
