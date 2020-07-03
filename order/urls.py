from django.urls import path
from order.views import OrderCommitView, OrderInfoView, OrderFinishView

urlpatterns = [
    path('new/', OrderCommitView.as_view(), name='new'),
    path('order/info/', OrderInfoView.as_view(), name='info'),
    path('order/finish/', OrderFinishView.as_view(), name='finish'),
]
