from django.urls import path
from . import views

app_name = 'workflows'

urlpatterns = [
    path('', views.workflow_list, name='list'),
    path('create/', views.workflow_create, name='create'),
    path('<int:pk>/', views.workflow_canvas, name='canvas'),
    path('api/<int:pk>/save/', views.api_save_workflow, name='api_save'),
    path('api/<int:pk>/load/', views.api_load_workflow, name='api_load'),
]
