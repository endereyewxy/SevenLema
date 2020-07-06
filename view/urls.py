from django.urls import path
from .views import shop, register, dish, login, root

urlpatterns = [
    path('', root),

    path('register/',           register),
    path('login/',              login),
    path('index/',              shop),
    path('shop/<int:shop_id>/', dish),
]
