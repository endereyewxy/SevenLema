from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from cmdb.models.shop import Shop
from cmdb.models.dish import Dish
from datetime import datetime


# from django.contrib.auth.mixins import LoginRequiredMixin

# Order Commit View Part
class OrderCommitView(View):
    def post(self, request):
        # user login in check
        user = request.user
        # if not user.is_authenticated:
        #     return JsonResponse({'code': 103, 'msg': '请先登录'})
        # get post parameters
        shop_id = request.POST.get('shop_id')
        dish_id = request.POST.get('dish_id')
        amount = request.POST.get('amount')
        addr = request.POST.get('addr')
        loc_lng = request.POST.get('loc_lng')
        loc_lat = request.POST.get('loc_lat')
        remarks = request.POST.get('remarks')
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

        # dish exist checks
        disherror = {}
        for dish in dish_id:
            if not Dish.objects.filter(shop_id=shop_id, name=dish).exists():
                disherror[str(dish)] = 'dish is not in this shop'
                continue
            dish_obj = Dish.objects.get(shop_id=shop_id, name=dish)
            if not dish_obj.serving:
                disherror[str(dish)] = 'dish is not on sell'
        if disherror:
            # return JsonResponse({'code': 105, 'data': disherror})
            return JsonResponse(disherror)

        # creating order_id by time and user info
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        return JsonResponse({'code': 0, 'msg': "creating order succeed", 'data': order_id})


# 订单页面展示
class OrderInfoView(View):
    def post(self, request):
        # post参数
        order_id = request.POST.get('order_id')
        shop_id = request.POST.get('shop_id')
        page = request.POST.get('page')
        limit = request.POST.get('limit')
        unfinished = request.POST.get('unfinished')
        tm_ordered = request.POST.get('tm_ordered')
        tm_finished = request.POST.get('tm_finished')
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
        order_id = request.POST.get('order_id')
        # 参数检验

        return render(request, 'finished.html')
