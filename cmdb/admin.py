from django.contrib import admin
from .models.order import Order
from .models.dish import Dish
from .models.shop import Shop
from .models.user import User
from .models.tag import Tag

# Register your models here.
admin.site.register(Order)
admin.site.register(Dish)
admin.site.register(Shop)
admin.site.register(Tag)
admin.site.register(User)
