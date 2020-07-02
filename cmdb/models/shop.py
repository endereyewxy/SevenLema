from django.db import models

from .user import User


class Shop(models.Model):
    user_id = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=16)
    desc = models.TextField()
    addr = models.CharField(max_length=50)
    loc_lng = models.DecimalField(max_digits=9, decimal_places=5)
    loc_lat = models.DecimalField(max_digits=9, decimal_places=5)
    avg_price = models.FloatField(default=0.0)
    sales = models.IntegerField(default=0)
    phone = models.CharField(max_length=11)
    serving = models.BooleanField()
