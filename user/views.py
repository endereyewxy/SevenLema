from django.http import JsonResponse
from django.views.decorators.http import require_POST

from cmdb.models.user import User


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
def logout(request):
    if 'id' in request.session:
        del request.session['id']
        return JsonResponse({'code': 0, 'msg': '', 'data': None})
    else:
        return JsonResponse({'code': 103, 'msg': '用户尚未登录'})
