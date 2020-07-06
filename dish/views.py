import os
from hashlib import md5
from uuid import uuid4

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from cmdb.models.dish import Dish
from cmdb.models.user import User


def check_login_status(request):
    if 'id' in request.session:
        try:
            return True, User.objects.get(id=request.session['id'])
        except User.DoesNotExist:
            pass
    return False, JsonResponse({'code': 103, 'msg': '用户尚未登录'})


@require_POST
def create(request):
    pass


@require_POST
def edit(request):
    login, user = check_login_status(request)
    if not login:
        return user

    dish_id = request.POST.get('dish_id')
    if dish_id is None:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
    try:
        dish_id = int(dish_id)
    except ValueError:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})

    try:
        dish = Dish.objects.get(id=dish_id)
        if dish.shop.user_id != user.id:
            return JsonResponse({'code': 103, 'msg': '权限不足'})
    except Dish.DoesNotExist:
        return JsonResponse({'code': 102, 'msg': '菜品不存在'})

    name = request.POST.get('name')
    if name is not None:
        dish.name = name

    image = request.FILES.get('image')
    if image is not None:
        if image.size > 20480000:
            return JsonResponse({'code': 105, 'msg': '图片体积过大'})
        # Generate unique name
        ext = image.name.split('.')[-1]
        if ext not in ['png', 'jpg', 'svg']:
            return JsonResponse({'code': 105, 'msg': '图片类型不支持'})
        tok = md5(str(uuid4()).encode('utf-8')).hexdigest()[8:-12]
        with open(os.path.join(settings.STATIC_ROOT, tok + '.' + ext), 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        dish.image = tok + '.' + ext

    desc = request.POST.get('desc')
    if desc is not None:
        dish.desc = desc

    price = request.POST.get('price')
    if price is not None:
        try:
            price = float(price)
        except ValueError:
            return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
        dish.set_actual_price(price)

    serving = request.POST.get('serving')
    if serving is not None:
        dish.serving = serving == 'true'

    dish.save()
    return JsonResponse({'code': 0, 'msg': '', 'data': None})
