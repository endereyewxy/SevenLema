from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from SevenLema.utils import require_login, require_post_param, require_get_param, require_image
from cmdb.models.shop import Shop


@require_POST
@require_login
@require_post_param('name')
@require_post_param('desc')
@require_image()
@require_post_param('addr')
@require_post_param('loc_lng',   float)
@require_post_param('loc_lat',   float)
@require_post_param('avg_price', float)
@require_post_param('phone')
def create(request, user, name, image, desc, addr, loc_lng, loc_lat, avg_price, phone):
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
    shop.save()
    return JsonResponse({'code': 0, 'msg': '', 'data': {'shop_id': shop.id}})


@require_GET
@require_login
def mine(request, user):
    data = []
    for shop in Shop.objects.filter(user=user):
        obj = model_to_dict(shop)
        obj['shop_id'] = obj['id']
        del obj['id']
        obj['loc_lng'] = float(obj['loc_lng'])
        obj['loc_lat'] = float(obj['loc_lat'])
        obj['avg_price'] = shop.get_actual_avg_price()
        data.append(obj)
    return JsonResponse({'code': 0, 'msg': '', 'data': data})


@require_POST
@require_login
@require_post_param('shop_id',   int)
@require_post_param('name',      None,  False)
@require_image(False)
@require_post_param('desc',      None,  False)
@require_post_param('addr',      None,  False)
@require_post_param('loc_lng',   float, False)
@require_post_param('loc_lat',   float, False)
@require_post_param('avg_price', float, False)
@require_post_param('phone',     None,  False)
@require_post_param('serving',   bool,  False)
def edit(request, user, shop_id, name, image, desc, addr, loc_lng, loc_lat, avg_price, phone, serving):
    try:
        shop = Shop.objects.get(id=shop_id)
    except Shop.DoesNotExist:
        return JsonResponse({'code': 102, 'msg': '商户不存在'})
    if shop.user_id != user.id:
        return JsonResponse({'code': 105, 'msg': '商户必须在当前用户名下'})

    # Update shop data
    if name is not None:
        shop.name = name
    if image is not None:
        shop.image = image
    if desc is not None:
        shop.desc = desc
    if addr is not None:
        shop.addr = addr
    if loc_lng is not None:
        shop.loc_lng = loc_lng
    if loc_lat is not None:
        shop.loc_lat = loc_lat
    if avg_price is not None:
        shop.set_actual_avg_price(avg_price)
    if phone is not None:
        shop.phone = phone
    if serving is not None:
        shop.serving = serving
    shop.save()

    return JsonResponse({'code': 0, 'msg': '成功修改商家数据'})
