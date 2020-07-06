from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from cmdb.models.user import User


@require_POST
def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    addr     = request.POST.get('addr')
    loc_lng  = request.POST.get('loc_lng')
    loc_lat  = request.POST.get('loc_lat')
    phone    = request.POST.get('phone')

    if None in [username, password, phone] or len(phone) != 11:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
    if loc_lng is not None:
        try:
            loc_lng = float(loc_lng)
            loc_lat = float(loc_lat)
        except ValueError:
            return JsonResponse({'code': 101, 'msg': '参数类型不正确'})

    if User.objects.filter(username__exact=username).exists():
        return JsonResponse({'code': 104, 'msg': '用户名冲突'})

    user = User.objects.create(
        username=username,
        addr=    addr,
        loc_lng= loc_lng,
        loc_lat= loc_lat,
        phone=   phone)

    user.set_salt()

    user.set_password(password)
    user.save()

    request.session['id'] = user.id
    return JsonResponse({'code': 0, 'msg': 0, 'data': None})


@require_POST
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if None in [username, password]:
        return JsonResponse({'code': 101, 'msg': '参数类型不正确'})
    try:
        user = User.objects.get(username__exact=username)
        if user.check_password(password):
            request.session['id'] = user.id
            return JsonResponse({'code': 0, 'msg': '', 'data': None})
    except User.DoesNotExist:
        pass
    return JsonResponse({'code': 103, 'msg': '登录失败'})


@require_POST
@csrf_exempt
def logout(request):
    if 'id' in request.session:
        del request.session['id']
        return JsonResponse({'code': 0, 'msg': '', 'data': None})
    else:
        return JsonResponse({'code': 103, 'msg': '用户尚未登录'})
