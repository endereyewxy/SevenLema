from django.http import JsonResponse
from django.views.decorators.http import require_POST

from SevenLema.utils import require_login, require_post_param, require_image
from cmdb.models.dish import Dish
from cmdb.models.shop import Shop


@require_POST
@require_login
@require_post_param('shop_id', int)
@require_post_param('name')
@require_image()
@require_post_param('desc')
@require_post_param('price',   float)
def create(request, user, shop_id, name, image, desc, price):
    try:
        shop = Shop.objects.get(id=shop_id)
    except Shop.DoesNotExist:
        return JsonResponse({'code': 102, 'msg': '商户不存在'})
    if shop.user_id != user.id:
        return JsonResponse({'code': 105, 'msg': '商户必须在当前用户名下'})
    dish = Dish.objects.create(
        shop_id=shop_id,
        name   =name,
        image  =image,
        desc   =desc,
        sales  =0,
        serving=True)
    dish.set_actual_price(price)
    dish.save()
    return JsonResponse({'code': 0, 'msg': '', 'data': {'dish_id': dish.id}})


@require_POST
@require_login
@require_post_param('dish_id', int)
@require_post_param('name',    None,  False)
@require_image(False)
@require_post_param('desc',    None,  False)
@require_post_param('price',   float, False)
@require_post_param('serving', bool,  False)
def edit(request, user, dish_id, name, image, desc, price, serving):
    try:
        dish = Dish.objects.get(id=dish_id)
        if dish.shop.user_id != user.id:
            return JsonResponse({'code': 103, 'msg': '权限不足'})
    except Dish.DoesNotExist:
        return JsonResponse({'code': 102, 'msg': '菜品不存在'})
    if dish.shop.user_id != user.id:
        return JsonResponse({'code': 105, 'msg': '商户必须在当前用户名下'})

    if name is not None:
        dish.name = name
    if image is not None:
        dish.image = image
    if desc is not None:
        dish.desc = desc
    if price is not None:
        dish.set_actual_price(price)
    if serving is not None:
        dish.serving = serving
    dish.save()
    return JsonResponse({'code': 0, 'msg': '', 'data': None})
