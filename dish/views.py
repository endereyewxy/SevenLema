from django.http import JsonResponse
from django.views.decorators.http import require_POST

from SevenLema.utils import upload_image, check_login_status
from cmdb.models.dish import Dish


@require_POST
def create(request):
    login, user = check_login_status(request)
    if not login:
        return user

    shop_id = request.POST.get('shop_id')
    name    = request.POST.get('name')
    image   = request.POST.get('image')
    desc    = request.POST.get('desc')
    price   = request.POST.get('price')

    if None in [shop_id, name, image, desc, price]:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})

    try:
        dish = Dish.objects.create(
            shop_id=shop_id,
            name   =name,
            image  =image,
            desc   =desc,
            price  =0,
            sales  =0,
            serving=True)
        dish.set_actual_price(float(price))
    except ValueError:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
    dish.save()

    return JsonResponse({'code': 0, 'msg': '', 'data': {'dish_id': dish.id}})


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
        dish.image = upload_image(image)

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
