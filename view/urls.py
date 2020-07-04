from django.urls import path
from .views import shop, register, dish, root

urlpatterns = [
    path('', root),
    path('register/', register),
    path('index/', shop),
    path('shop/<int:shop_id>/', dish)
]
