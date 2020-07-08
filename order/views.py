import time

from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from SevenLema.utils import require_login, add_page_info, require_post_param, require_get_param
from cmdb.models.dish import Dish
from cmdb.models.dish_order import DishOrder
from cmdb.models.order import Order
from cmdb.models.shop import Shop


@require_POST
@require_login
@require_post_param('shop_id', int)
@require_post_param('addr')
@require_post_param('loc_lng', float)
@require_post_param('loc_lat', float)
@require_post_param('remarks')
def new(request, user, shop_id, addr, loc_lng, loc_lat, remarks):
    # Get post parameters
    dish_ids = request.POST.getlist('dish_id[]')
    amounts  = request.POST.getlist('amount[]')
    if None in [dish_ids, amounts]:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
    try:
        dish_ids = [int(x) for x in dish_ids]
        amounts  = [int(x) for x in amounts]
    except ValueError:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})

    # Existence of shop_id check and whether on serving time check
    try:
        shop = Shop.objects.get(id=shop_id)
        if not shop.serving:
            return JsonResponse({'code': 106, 'msg': '商户未营业'})
        if shop.user_id == user.id:
            return JsonResponse({'code': 105, 'msg': '无法在此店下单'})
    except Shop.DoesNotExist:
        return JsonResponse({'code': 102, 'msg': '商户不存在'})

    # Dish validness check
    for dish_id in dish_ids:
        try:
            dish = Dish.objects.get(id=dish_id)
            if not dish.serving:
                return JsonResponse({'code': 106, 'msg': '菜品 {0} 暂时缺货'.format(dish_id)})
            if dish.shop_id != shop_id:
                return JsonResponse({'code': 105, 'msg': '菜品 {0} 不属于商户 {1}'.format(dish.name, shop.name)})
        except Dish.DoesNotExist:
            return JsonResponse({'code': 102, 'msg': '菜品不存在'})

    # Create order
    order = Order.objects.create(
        user       =user,
        shop       =shop,
        remarks    =remarks,
        addr       =addr,
        loc_lng    =loc_lng,
        loc_lat    =loc_lat,
        tm_ordered =int(time.time()),
        tm_finished=None)
    order.save()
    for dish_id, amount in zip(dish_ids, amounts):
        dish = Dish.objects.get(id=dish_id)
        DishOrder.objects.create(
            dish  =dish,
            order =order,
            amount=amount)
        dish.sales += amount
        dish.save()
    shop.sales += 1
    shop.save()

    return JsonResponse({'code': 0, 'msg': '', 'data': {'order_id': order.id}})


def order_info(order):
    json = model_to_dict(order)
    json['username']  = order.user.username
    json['user_phone'] = order.user.phone
    json['shop_name'] = order.shop.name
    json['dishes']    = []
    for dish_order in DishOrder.objects.filter(order_id=order.id):
        dish = Dish.objects.get(id=dish_order.dish_id)
        json['dishes'].append({
            'dish_id': dish.id,
            'name':    dish.name,
            'amount':  dish_order.amount
        })
    return json


@require_GET
@require_login
@require_get_param('order_id',   int, False)
@require_get_param('shop_id',    int, False)
@require_get_param('page',       int)
@require_get_param('limit',      int)
@require_get_param('unfinished', bool, False)
def info(request, user, order_id, shop_id, page, limit, unfinished):
    try:
        # User get order info
        if order_id is not None:
            order = Order.objects.get(id=int(order_id))
            if user.id != order.user_id:
                return JsonResponse({'code': 103, 'msg': '权限不足'})
            if page == 1 and (not unfinished or order.tm_finished is None):
                return JsonResponse({'code': 0, 'msg': '', 'page': 1, 'data': [order_info(order)]})
            else:
                return JsonResponse({'code': 0, 'msg': '', 'page': 1, 'data': []})

        # Shop get order info
        elif shop_id is not None:
            shop = Shop.objects.get(id=int(shop_id))
            if shop.user_id != user.id:
                return JsonResponse({'code': 103, 'msg': '权限不足'})
            qs = Order.objects.filter(shop_id=shop_id)
        else:
            qs = Order.objects.filter(user=user)
    except ValueError:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})

    if unfinished:
        qs = qs.filter(tm_finished=None)
    qs, max_page = add_page_info(qs, page, limit)
    data = []
    for order in qs:
        data = [order_info(order)] + data
    return JsonResponse({'code': 0, 'msg': '', 'page': max_page, 'data': data})


@require_POST
@require_login
@require_post_param('order_id', int)
def finish(request, user, order_id):
    # User connection check
    try:
        order = Order.objects.get(id=order_id)
        if order.shop.user.id != user.id:
            return JsonResponse({'code': 103, 'msg': '权限不足'})
    except Order.DoesNotExist:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})

    # Order state check
    if order.tm_finished is not None:
        return JsonResponse({'code': 105, 'msg': '订单已经送达'})

    order.tm_finished = int(time.time())
    order.save()

    return JsonResponse({'code': 0, 'msg': ''})
