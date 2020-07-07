from math import floor

from django.db import models

from .user import User


class Shop(models.Model):
    user      = models.ForeignKey(User, models.CASCADE)
    name      = models.CharField(max_length=50)
    image     = models.CharField(max_length=36)
    desc      = models.TextField()
    addr      = models.CharField(max_length=50)
    loc_lng   = models.DecimalField(max_digits=9, decimal_places=5)
    loc_lat   = models.DecimalField(max_digits=9, decimal_places=5)
    avg_price = models.FloatField(default=0.0)
    sales     = models.IntegerField(default=0)
    phone     = models.CharField(max_length=11)
    serving   = models.BooleanField(default=True)

    def get_actual_avg_price(self):
        """Get the actual average price unit by yuan"""
        return 0.01 * self.avg_price

    def set_actual_avg_price(self, avg_price):
        """Set the actual average price unit by yuan"""
        self.avg_price = floor(100 * avg_price)
