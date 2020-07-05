from django.urls import path
from order.views import new, info, finish

urlpatterns = [
    path('new/',    new),
    path('info/',   info),
    path('finish/', finish),
]
