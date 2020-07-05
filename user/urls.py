from django.urls import path

from user.views import login, logout, register

urlpatterns = [
    path('register/', register),
    path('login/',    login),
    path('logout/',   logout),
]
