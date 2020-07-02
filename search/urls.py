# Developer: endereye <endereyewxy@gmail.com>

from django.urls import path

from . import views

urlpatterns = [
    path('shop/', views.shop),
    path('dish/', views.dish)
]