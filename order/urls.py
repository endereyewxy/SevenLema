from django.urls import path
from order.views import OrderCommitView

urlpatterns = [
    path('new/', OrderCommitView.as_view(), name='new')
]
