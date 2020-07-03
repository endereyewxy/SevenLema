from django.urls import path
from .views import shop, register

urlpatterns = [
    path('register', register),
    path('index', shop)
]
