from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from cmdb.models.user import User
from cmdb.models.shop import Shop
from cmdb.models.dish import Dish
from datetime import datetime
import json


# from django.contrib.auth.mixins import LoginRequiredMixin

# Order Commit View Part
class OrderCommitView(View):
    def post(self, request):
        # user login in check
        # user = request.user
        # if not user.is_authenticated:
        #     return JsonResponse({'code': 103, 'msg': '请先登录'})
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
            shop_selected = Shop.objects.get(id=shop_id)
            # print(shop_selected.serving)
            if not shop_selected.serving:
                return JsonResponse({'code': 106, 'msg': 'shop no serving time'})
        except Shop.DoesNotExist:
            return JsonResponse({'code': 106, 'msg': 'shop no exist'})

        # dish connection and exist checks
        dishError = {}
        for dish in dish_id:
            if not Dish.objects.filter(shop_id=shop_id, name=dish).exists():
                # dishError[str(dish)] = 'dish is not in this shop'
                # 'dish {0} is not in the shop{1}'.format(dish, shop_id)
                dishError.setdefault(105, []).append('dish {0} not in the shop {1}'.format(dish, shop_id))
                continue
            dish_obj = Dish.objects.get(shop_id=shop_id, name=dish)
            if not dish_obj.serving:
                # dishError[str(dish)] = 'dish is not on sell'
                dishError.setdefault(106, []).append('dish {0} not on sale'.format(dish))
        if dishError:
            data = json.dumps(dishError)
            return JsonResponse(data, safe=False)

        # creating order_id by time and user info
        order_id = datetime.now().strftime('%Y%m%d%H%M') + str(shop_id)
        return JsonResponse({'code': 0, 'msg': "creating order succeed", 'data': order_id})


# 订单页面展示
class OrderInfoView(View):
    def post(self, request):
        # post参数
        res = request.body
        order_id = res['order_id']
        shop_id = res['shop_id']
        page = res['page']
        limit = res['limit']
        unfinished = res['unfinished']
        tm_ordered = res['tm_ordered']
        tm_finished = res['tm_finished']
        # 参数检验
        context = {
            'user_id': 0,
            'username': 0,
            'phone': 0,
            'shop_id': 0,
            'shop_name': 0,
            'dishes': 0,
            'addr': 0,
            'loc_lng': 0,
            'loc_lat': 0,
            'remarks': 0,
            'tm_ordered': 0,
            'tm_finished': 0,
        }
        # 参数传回
        return JsonResponse({'code': 0, 'msg': "creating order succeed", 'data': context})


class OrderFinishView(View):
    def post(self, request):
        # post参数
        # 参数检验
        pass
