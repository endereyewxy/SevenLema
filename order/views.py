from django.shortcuts import render
from django.views import View
from django.http import JsonResponse


# 前端post传递参数，包括user,shop,amount,addr,loc_lng,loc_lat
class OrderCommitView(View):
    def post(self, request):
        # 用户登录检测

        # 获取post参数
        user = request.POST.get('user_id')
        shop = request.POST.get('shop_id')
        amount = request.POST.get('amount')
        addr = request.POST.get('addr')
        loc_lng = request.POST.get('loc_lng')
        loc_lat = request.POST.get('loc_lat')
        tm_ordered = request.POST.get('tm_ordered')
        tm_finished = request.POST.get('tm_finished')

        # 成功后返回数据 订单号 随机生成
        order_id = 1
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
        return render(request, 'new.html', context)


class OrderFinishView(View):
    def post(self, request):
        # post参数
        order_id = request.POST.get('order_id')
        # 参数检验

        return render(request, 'finished.html')
