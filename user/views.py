from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from SevenLema.utils import require_login, require_post_param
from cmdb.models.user import User


@require_POST
@require_post_param('username')
@require_post_param('password')
@require_post_param('addr')
@require_post_param('loc_lng', float)
@require_post_param('loc_lat', float)
@require_post_param('phone')
def register(request, username, password, addr, loc_lng, loc_lat, phone):
    if User.objects.filter(username__exact=username).exists():
        return JsonResponse({'code': 104, 'msg': '用户名冲突'})

    user = User.objects.create(
        username=username,
        addr    =addr,
        loc_lng =loc_lng,
        loc_lat =loc_lat,
        phone   =phone
    )
    user.set_salt()
    user.set_password(password)
    user.save()

    request.session['id'] = user.id
    return JsonResponse({'code': 0, 'msg': 0, 'data': None})


@require_POST
@require_post_param('username')
@require_post_param('password')
def login(request, username, password):
    try:
        user = User.objects.get(username__exact=username)
        if user.check_password(password):
            request.session['id'] = user.id
            return JsonResponse({'code': 0, 'msg': '', 'data': None})
    except User.DoesNotExist:
        pass
    return JsonResponse({'code': 103, 'msg': '登录失败'})


@require_POST
@require_login
@csrf_exempt
def logout(request, user):
    assert user.id == request.session['id']  # tell PyCharm that we did use the user parameter
    del request.session['id']
    return JsonResponse({'code': 0, 'msg': '', 'data': None})
