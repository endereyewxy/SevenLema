import json
import time

from django.http import JsonResponse
from django.views import View

from cmdb.models.dish import Dish
from cmdb.models.dish_order import DishOrder
from cmdb.models.order import Order
from cmdb.models.shop import Shop
from cmdb.models.user import User


# Order Commit View Part
class OrderCommitView(View):
    def post(self, request):
        # user login in check
        if 'id' in request.session:
            user_id = request.session['id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'code': 103, 'msg': 'no login in '})
        else:
            return JsonResponse({'code': 103, 'msg': 'no login in '})
        # get post parameters
        data = request.body
        res = json.loads(data)

        shop_id = res['shop_id']
        dish_id = res['dish_id']
        amount = res['amount']
        addr = res['addr']
        loc_lng = res['loc_lng']
        loc_lat = res['loc_lat']
        remarks = res['remarks']
        # necessary parameters checks
        if not all([shop_id, dish_id, amount, addr, loc_lng, loc_lat, remarks]):
            return JsonResponse({'code': 101, 'msg': 'parameters lost'})

        # shop_id exist check and whether on serving time check
        try:
            shop = Shop.objects.get(id=shop_id)
            if not shop.serving:
                return JsonResponse({'code': 106, 'msg': 'shop no serving time'})
        except Shop.DoesNotExist:
            return JsonResponse({'code': 106, 'msg': 'shop no exist'})

        # dish connection and exist checks
        dish_error = {}
        for dish in dish_id:
            if not Dish.objects.filter(shop_id=shop_id, name=dish).exists():
                # 'dish {0} is not in the shop{1}'.format(dish, shop_id)
                dish_error.setdefault(105, []).append('dish {0} not in the shop {1}'.format(dish, shop_id))
                continue
            dish_obj = Dish.objects.get(shop_id=shop_id, name=dish)
            if not dish_obj.serving:
                dish_error.setdefault(106, []).append('dish {0} not on sale'.format(dish))
        if dish_error:
            data = json.dumps(dish_error)
            return JsonResponse(data, safe=False)

        # creating order_id by time and user info
        order = Order.objects.create(
            user_id=user,
            shop_id=shop,
            remarks=remarks,
            addr=addr,
            loc_lng=loc_lng,
            loc_lat=loc_lat,
            tm_ordered=int(time.time()),
            tm_finished=False
        )
        order.save()
        order_id = order.id
        for index in range(len(dish_id)):
            dish_index = dish_id[index]
            dish_in = Dish.objects.get(shop_id=shop_id, name=dish_index)
            amount_in = int(amount[index])
            DishOrder.objects.create(
                dish_id=dish_in,
                order_id=order,
                amount=amount_in
            )

        return JsonResponse({'code': 0, 'msg': "creating order succeed", 'data': order_id})


def order_info(order_id, context):
    order = Order.objects.get(id=order_id)
    user = order.user_id
    shop = order.shop_id
    context.append({'user_id': user.id})
    context.append({'user_name': user.username})
    context.append({'user_id': user.phone})
    context.append({'shop_id': shop.id})
    context.append({'shop_name': shop.name})
    dish_orders = DishOrder.objects.filter(order_id=order_id).all()
    for dish_order in dish_orders:
        dish = dish_order.dish_id
        dish_id = dish.id
        name = dish.name
        amount = dish_order.amount
        data = {'dish_id': dish_id, 'name': name, 'amount': amount}
        context.append(data)
    context.append({'loc_lng': user.loc_lng})
    context.append({'loc_lat': user.loc_lat})
    context.append({'remarks': order.remarks})
    context.append({'tm_ordered': order.tm_ordered})
    context.append({'tm_finished': order.tm_finished})


# 订单页面展示
class OrderInfoView(View):
    def post(self, request):
        # user login in check
        if 'id' in request.session:
            user_id = request.session['id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'code': 103, 'msg': 'no login in '})
        else:
            return JsonResponse({'code': 103, 'msg': 'no login in '})

        # get post parameters
        data = request.body
        res = json.loads(data)
        page = res['page']
        limit = res['limit']
        unfinished = res['unfinished']

        context = []
        # user get order info
        if 'order_id' in res:
            order_id = res['order_id']
            order = Order.objects.get(id=order_id)
            user = order.user_id
            # user check
            if user.id != user_id:
                return JsonResponse({'code': 103, 'msg': "no right to see the user order "})
            order_info(order_id, context)
            return JsonResponse({'code': 0, 'msg': "get order info succeed", 'data': context})
        # shop get order info
        elif 'shop_id' in res:
            shop_id = res['shop_id']
            if shop_id != user_id:
                return JsonResponse({'code': 103, 'msg': "no right to see the shop order "})
            shop = Order.objects.get(id=shop_id)
            orders = Order.objects.filter(shop_id=shop_id)
            for order in orders:
                order_info(order.id, context)
            return JsonResponse({'code': 0, 'msg': "get order info succeed", 'data': context})
        # no useful input
        else:
            return JsonResponse({'code': 103, 'msg': "no order_id and shop_id input "})


class OrderFinishView(View):
    def post(self, request):
        # user login in check
        if 'id' in request.session:
            user_id = request.session['id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'code': 103, 'msg': 'no login in '})
        else:
            return JsonResponse({'code': 103, 'msg': 'no login in '})

        # get post parameters
        data = request.body
        res = json.loads(data)
        order_id = res['order_id']
        if not order_id:
            return JsonResponse({'code': 101, 'msg': 'parameters lost'})

        # user connection check
        order = Order.objects.get(id=order_id)
        if order_id != user_id:
            return JsonResponse({'code': 103, 'msg': 'order not belong to this user '})
        # order state check
        if not order.tm_finished:
            return JsonResponse({'code': 105, 'msg': 'order not finish now'})

        return JsonResponse({'code': 0, 'msg': 'order finish'})
