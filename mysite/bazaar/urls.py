from django.urls import path
from . import  views

urlpatterns = [
    path('', views.home, name='bazaar-home'),
    path('about/', views.about, name='bazaar-about'),
]
