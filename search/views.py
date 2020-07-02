# Developer: endereye <endereyewxy@gmail.com>

from math import radians

from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from cmdb.models import Shop, Dish


def shop_to_json(order, obj):
    json = {
            'shop_id':   obj.id,
            'name':      obj.name,
            'image':     obj.image,
            'desc':      obj.desc,
            'addr':      obj.addr,
            'loc_lng':   float(obj.loc_lng),
            'loc_lat':   float(obj.loc_lat),
            'avg_price': obj.get_actual_avg_price(),
            'sales':     obj.sales,
            'phone':     obj.phone,
            'serving':   obj.serving
        }
    if order == 'dist':
        json['dist'] = 1000 * float(obj.dist)
    return json


def dish_to_json(obj):
    return {
        'dish_id': obj.id,
        'name':    obj.name,
        'image':   obj.image,
        'desc':    obj.desc,
        'price':   obj.get_actual_price(),
        'sales':   obj.sales,
        'serving': obj.serving
    }


@require_GET
def shop(request):
    # Fetch general parameters
    name    = request.GET.get('name')
    order   = request.GET.get('order')
    # TODO implement tags
    # tags    = request.GET.getlist('tags', [])
    page    = request.GET.get('page')
    limit   = request.GET.get('limit')
    serving = request.GET.get('serving')

    # Check validness
    if None in [name, order] or not (page + limit).isdigit():
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})

    # Convert parameters to their actual type
    page    = int(page)
    limit   = int(limit)
    serving = serving == 'true'

    # Perform queries
    qs = Shop.objects.filter(name__icontains=name)
    if serving:
        qs = qs.filter(serving__exact=True)

    # Sort results
    if order == 'dist':
        # Fetch location parameters
        loc_lng = request.GET.get('loc_lng')
        loc_lat = request.GET.get('loc_lat')

        # Check validness and covert to actual type
        if None in [loc_lng, loc_lat]:
            return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
        try:
            loc_lng = radians(float(loc_lng))
            loc_lat = radians(float(loc_lat))
        except ValueError:
            return JsonResponse({'code': 101, 'msg': '参数类型不正确'})

        # Perform raw SQL query
        sql = """
        SELECT  *, (
            6378.137 * acos(
                cos({1})
                * cos(radians(loc_lat))
                * cos(radians(loc_lng) - {0})
                + sin({1})
                * sin(radians(loc_lat))
            )
        ) AS dist FROM cmdb_shop ORDER BY dist""".replace('{0}', str(loc_lng)).replace('{1}', str(loc_lat))
        qs = qs.raw(sql)

    elif order == 'avg_price':
        qs = qs.order_by('avg_price')
    elif order == 'sales':
        qs = qs.order_by('-sales')
    else:
        return JsonResponse({'code': 101, 'msg': '排序方式不支持'})

    # Add page information
    try:
        qs = Paginator(qs, limit).page(page)
    except EmptyPage:
        qs = []

    # Change query set into dictionaries
    return JsonResponse({'code': 0, 'msg': '', 'data': [shop_to_json(order, obj) for obj in qs]})


@require_GET
def dish(request):
    # Fetch general parameters
    shop_id = request.GET.get('shop_id')
    name    = request.GET.get('name')
    order   = request.GET.get('order')
    page    = request.GET.get('page')
    limit   = request.GET.get('limit')
    serving = request.GET.get('serving')

    # Check validness
    if None in [shop_id, name, order, page, limit] or not (page + limit).isdigit():
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})

    # Convert parameters to their actual types
    shop_id = int(shop_id)
    page    = int(page)
    limit   = int(limit)
    serving = serving == 'true'

    # Verify shop_id exists
    if not Shop.objects.filter(id=shop_id).exists():
        return JsonResponse({'code': 102, 'msg': '商户不存在'})

    # Perform queries
    qs = Dish.objects.filter(shop_id__exact=shop_id, name__icontains=name)
    if serving:
        qs = qs.filter(serving__exact=True)

    # Sort results
    if order == 'price':
        qs = qs.order_by('price')
    elif order == 'sales':
        qs = qs.order_by('-sales')
    else:
        return JsonResponse({'code': 101, 'msg': '排序方式不支持'})

    # Add page information
    try:
        qs = Paginator(qs, limit).page(page)
    except EmptyPage:
        qs = []

    # Change query into dictionaries
    return JsonResponse({'code': 0, 'msg': '', 'data': [dish_to_json(obj) for obj in qs]})
