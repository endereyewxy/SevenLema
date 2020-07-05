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
def create(request):
    # login in check
    login, user = check_login_status(request)
    if not login:
        return user

    # Get post parameters
    name = request.POST.get('name')
    image = request.POST.get('image')
    desc = request.POST.get('desc')
    addr = request.POST.get('addr')
    loc_lng = request.POST.get('loc_lng')
    loc_lat = request.POST.get('loc_lat')
    avg_price = request.POST.get('avg_price')
    phone = request.POST.get('phone')

    # Necessarily parameter checks
    if not all([name, image, desc, addr, loc_lng, loc_lat, avg_price, phone]):
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})

    # create shop in current user
    shop = Shop.objects.create(
        user=user,
        name=name,
        image=image,
        desc=desc,
        addr=addr,
        loc_lng=loc_lng,
        loc_lat=loc_lat,
        avg_price=avg_price,
        sales=0,
        phone=phone,
        serving=True,
    )
    shop.save()
    return JsonResponse({'code': 0, 'msg': '', 'data': {'shop_id': shop.id}})


def edit(request):
    # login in check
    login, user = check_login_status(request)
    if not login:
        return user

    # Get post parameters
    data = request.POST

    # Necessarily parameter checks
    if 'shop_id' not in data or len(data) <= 1:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
    shop_id = data.get('shop_id')
    shop = Shop.objects.filter(id=shop_id)
    if (Shop.objects.get(id=shop_id).user.id != user.id):
        return JsonResponse({'code': 102, 'msg': '商户必须在当前用户名下'})

    # update shop data/
    for key, value in data.items():
        if (key == 'name'):
            shop.update(name=value)
        elif (key == 'image'):
            shop.update(image=value)
        elif (key == 'desc'):
            shop.update(desc=value)
        elif (key == 'addr'):
            shop.update(addr=value)
        elif (key == 'loc_lng'):
            shop.update(loc_lng=value)
        elif (key == 'loc_lat'):
            shop.update(loc_lat=value)
        elif (key == 'avg_price'):
            shop.update(avg_price=value)
        elif (key == 'phone'):
            shop.update(phone=value)
    return JsonResponse({'code': 0, 'msg': '成功修改商家数据'})
