from django.urls import path

from user.views import login, logout

urlpatterns = [
    path('login/', login),
    path('logout/', logout)
]
