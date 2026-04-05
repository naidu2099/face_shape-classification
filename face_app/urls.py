from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('generate/', views.generate, name='generate'),
    path('regenerate/', views.regenerate, name='regenerate'),
]
