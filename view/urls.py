from django.urls import path
from .views import shop, register, dish

urlpatterns = [
    path('register/', register),
    path('index/', shop),
    path('shop/<int:shop_id>/', dish)
]
