from django.db import models

from .shop import Shop
from .user import User


class Order(models.Model):
    user_id = models.ForeignKey(User, models.CASCADE)
    shop_id = models.ForeignKey(Shop, models.CASCADE)
    remarks = models.CharField(max_length=50)
    addr = models.CharField(max_length=50)
    loc_lng = models.DecimalField(max_digits=9, decimal_places=5)
    loc_lat = models.DecimalField(max_digits=9, decimal_places=5)
    tm_ordered = models.BigIntegerField()
    tm_finished = models.BigIntegerField(null=True)
