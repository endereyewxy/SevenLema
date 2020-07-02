from django.db import models

from .dish import Dish
from .order import Order


class DishOrder(models.Model):
    dish_id = models.ForeignKey(Dish, models.CASCADE)
    order_id = models.ForeignKey(Order, models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        unique_together = ('dish_id', 'order_id')