from django.urls import path
from shop.views import create, edit, mine

urlpatterns = [
    path('create/', create),
    path('mine/',   mine),
    path('edit/',   edit),
]
