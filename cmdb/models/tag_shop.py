from django.db import models

from .shop import Shop
from .tag import Tag


class TagShop(models.Model):
    shop = models.ForeignKey(Shop, models.CASCADE)
    tag = models.ForeignKey(Tag, models.CASCADE)

    class Meta:
        unique_together = ('shop_id', 'tag_id')