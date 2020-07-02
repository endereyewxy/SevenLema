from math import floor

from django.db import models

from .shop import Shop


class Dish(models.Model):
    shop = models.ForeignKey(Shop, models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=16)
    desc = models.TextField()
    price = models.IntegerField()
    sales = models.IntegerField()
    serving = models.BooleanField(default=True)

    def get_actual_price(self):
        """Get the actual price unit by yuan"""
        return 0.01 * self.price

    def set_actual_price(self, price):
        """Set the actual price unit by yuan"""
        self.price = floor(price * 100)
