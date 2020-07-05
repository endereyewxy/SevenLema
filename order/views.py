import time

from django.core.paginator import Paginator, EmptyPage
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from cmdb.models.dish import Dish
from cmdb.models.dish_order import DishOrder
from cmdb.models.order import Order
from cmdb.models.shop import Shop
from cmdb.models.user import User


def check_login_status(request):
    if 'id' in request.session:
        try:
            return True, User.objects.get(id=request.session['id'])
        except User.DoesNotExist:
            pass
    return False, JsonResponse({'code': 103, 'msg': '用户尚未登录'})


@require_POST
def new(request):
    login, user = check_login_status(request)
    if not login:
        return user

    # Get post parameters
    shop_id  = request.POST.get('shop_id')
    dish_ids = request.POST.getlist('dish_id[]')
    amounts  = request.POST.getlist('amount[]')
    addr     = request.POST.get('addr')
    loc_lng  = request.POST.get('loc_lng')
    loc_lat  = request.POST.get('loc_lat')
    remarks  = request.POST.get('remarks')

    # Necessarily parameter checks
    if None in [shop_id, dish_ids, amounts, addr, loc_lng, loc_lat, remarks] or len(dish_ids) != len(amounts):
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
    try:
        shop_id = int(shop_id)
        dish_ids = [int(x) for x in dish_ids]
        amounts  = [int(x) for x in amounts]
        loc_lng = float(loc_lng)
        loc_lat = float(loc_lat)
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


def add_page_info(qs, page, limit):
    max_page = 0
    try:
        paginator = Paginator(qs, limit)
        max_page  = paginator.num_pages
        qs        = paginator.page(page)
    except EmptyPage:
        qs        = []
    return qs, max_page


@require_GET
def info(request):
    login, user = check_login_status(request)
    if not login:
        return user

    # Get post parameters
    order_id   = request.GET.get('order_id')
    shop_id    = request.GET.get('shop_id')
    page       = request.GET.get('page')
    limit      = request.GET.get('limit')
    unfinished = request.GET.get('unfinished')

    if not all([page, limit, unfinished]):
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
    try:
        page       = int(page)
        limit      = int(limit)
        unfinished = unfinished == 'true'
    except ValueError:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})

    # User get order info
    if order_id is not None:
        try:
            order_id = int(order_id)
        except ValueError:
            return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
        order = Order.objects.get(id=order_id)
        if user.id != order.user_id:
            return JsonResponse({'code': 103, 'msg': '权限不足'})
        if page == 1 and (not unfinished or order.tm_finished is None):
            return JsonResponse({'code': 0, 'msg': '', 'page': 1, 'data': [order_info(order)]})
        else:
            return JsonResponse({'code': 0, 'msg': '', 'page': 1, 'data': []})

    # Shop get order info
    elif shop_id is not None:
        try:
            shop_id = int(shop_id)
        except ValueError:
            return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
        shop = Shop.objects.get(id=shop_id)
        if shop.user_id != user.id:
            return JsonResponse({'code': 103, 'msg': '权限不足'})
        qs = Order.objects.filter(shop_id=shop_id)
        if unfinished:
            qs = qs.filter(tm_finished=None)
        qs, max_page = add_page_info(qs, page, limit)
        data = []
        for order in qs:
            data.append(order_info(order))
        return JsonResponse({'code': 0, 'msg': '', 'page': max_page, 'data': data})

    # No useful input
    else:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})


@require_POST
def finish(request):
    login, user = check_login_status(request)
    if not login:
        return user

    # Get post parameters
    order_id = request.POST.get('order_id')
    if order_id is None:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
    try:
        order_id = int(order_id)
    except ValueError:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})

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
