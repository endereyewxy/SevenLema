from django.urls import path
from order.views import OrderCommitView, OrderInfoView, OrderFinishView

urlpatterns = [
    path('new/', OrderCommitView.as_view(), name='new'),
    path('info/', OrderInfoView.as_view(), name='info'),
    path('finish/', OrderFinishView.as_view(), name='finish'),
]
