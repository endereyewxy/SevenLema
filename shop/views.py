from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from SevenLema.utils import check_login_status, upload_image
from cmdb.models.shop import Shop


@require_POST
def create(request):
    # Login in check
    login, user = check_login_status(request)
    if not login:
        return user

    # Get post parameters
    name      = request.POST.get('name')
    desc      = request.POST.get('desc')
    addr      = request.POST.get('addr')
    image     = request.FILES.get('image')
    loc_lng   = request.POST.get('loc_lng')
    loc_lat   = request.POST.get('loc_lat')
    avg_price = request.POST.get('avg_price')
    phone     = request.POST.get('phone')

    # Necessarily parameter checks
    if None in [name, image, desc, addr, loc_lng, loc_lat, avg_price, phone]:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
    ok, image = upload_image(image)
    if not ok:
        return image

    # Create shop in current user
    try:
        shop = Shop.objects.create(
            user     =user,
            name     =name,
            image    =image,
            desc     =desc,
            addr     =addr,
            loc_lng  =loc_lng,
            loc_lat  =loc_lat,
            avg_price=avg_price,
            sales    =0,
            phone    =phone,
            serving  =True)
    except ValueError:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
    shop.save()
    return JsonResponse({'code': 0, 'msg': '', 'data': {'shop_id': shop.id}})


@require_GET
def mine(request):
    login, user = check_login_status(request)
    if not login:
        return user

    data = []
    for shop in Shop.objects.filter(user=user):
        obj = model_to_dict(shop)
        obj['shop_id'] = obj['id']
        del obj['id']
        obj['loc_lng'] = float(obj['loc_lng'])
        obj['loc_lat'] = float(obj['loc_lat'])
        obj['avg_price'] = shop.get_actual_avg_price()
    return JsonResponse({'code': 0, 'msg': '', 'data': data})


@require_POST
def edit(request):
    # Login in check
    login, user = check_login_status(request)
    if not login:
        return user

    # Get post parameters
    data = request.POST

    # Necessarily parameter checks
    if 'shop_id' not in data or len(data) <= 1:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
    shop_id = data.get('shop_id')
    try:
        shop = Shop.objects.get(id=int(shop_id))
    except ValueError:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
    except Shop.DoesNotExist:
        return JsonResponse({'code': 102, 'msg': '商户不存在'})
    if shop.user_id != user.id:
        return JsonResponse({'code': 105, 'msg': '商户必须在当前用户名下'})

    # Update shop data
    try:
        for key, value in data.items():
            if key == 'name':
                shop.name = value
            elif key == 'desc':
                shop.desc = value
            elif key == 'addr':
                shop.addr = value
            elif key == 'loc_lng':
                shop.loc_lng = float(value)
            elif key == 'loc_lat':
                shop.loc_lat = float(value)
            elif key == 'avg_price':
                shop.set_actual_avg_price(float(value))
            elif key == 'phone':
                shop.phone = value
    except ValueError:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
    image = request.FILES.get('image')
    if image is not None:
        ok, image = upload_image(image)
        if not ok:
            return image
        shop.image = image
    shop.save()
    return JsonResponse({'code': 0, 'msg': '成功修改商家数据'})
