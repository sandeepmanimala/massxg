from django.urls import path
from . import views

app_name = 'research'

urlpatterns = [
    path('', views.paper_list, name='list'),
    path('submit/', views.paper_submit, name='submit'),
    path('<int:pk>/', views.paper_detail, name='detail'),
]
