from django.contrib import admin

from .models.dish import Dish
from .models.dish_order import DishOrder
from .models.order import Order
from .models.shop import Shop
from .models.tag import Tag
from .models.tag_shop import TagShop
from .models.user import User

admin.site.register(Dish)
admin.site.register(DishOrder)
admin.site.register(Order)
admin.site.register(Shop)
admin.site.register(Tag)
admin.site.register(TagShop)
admin.site.register(User)
