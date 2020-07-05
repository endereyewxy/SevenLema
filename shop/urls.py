from django.urls import path
from shop.views import create, edit

urlpatterns = [
    path('create/', create),
    path('edit/', edit),
]
