from django.urls import path

from dish.views import edit, create

urlpatterns = [
    path('create/', create),
    path('edit/',   edit),
]