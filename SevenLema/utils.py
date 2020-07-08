import os
from hashlib import md5
from uuid import uuid4

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse

from cmdb.models.user import User


def require_login(view):
    def wrapper(request, *args, **kwargs):
        if 'id' in request.session:
            try:
                kwargs['user'] = User.objects.get(id=request.session['id'])
                return view(request, *args, **kwargs)
            except User.DoesNotExist:
                pass
        return JsonResponse({'code': 103, 'msg': '用户尚未登录'})

    return wrapper


def __require_param(is_post, param, type_=None, required=True):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            arg = request.POST.get(param) if is_post else request.GET.get(param)
            if arg is None and not required:
                kwargs[param] = None
                return view(request, *args, **kwargs)
            if arg is not None:
                try:
                    kwargs[param] = arg if type_ is None else type_(arg)
                    return view(request, *args, **kwargs)
                except ValueError:
                    pass
            return JsonResponse({'code': 101, 'msg': '参数类型不正确'})

        return wrapper

    return decorator


def require_post_param(param, type_=None, required=True):
    return __require_param(True, param, type_, required)


def require_get_param(param, type_=None, required=True):
    return __require_param(False, param, type_, required)


def require_image(required=True):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            image = request.FILES.get('image')
            if image is not None:
                if image.size > 20480000:
                    return False, JsonResponse({'code': 105, 'msg': '图片体积过大'})
                ext = image.name.split('.')[-1]
                if ext not in ['svg', 'jpg', 'png', 'gif']:
                    return False, JsonResponse({'code': 101, 'msg': '图片格式不支持'})
                tok = md5(str(uuid4()).encode('utf-8')).hexdigest()
                with open(os.path.join(settings.STATIC_ROOT, 'images', tok + '.' + ext), 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                kwargs['image'] = tok + '.' + ext
                return view(request, *args, **kwargs)
            elif not required:
                kwargs['image'] = None
                return view(request, *args, **kwargs)
            return JsonResponse({'code': 101, 'msg': '参数类型不正确'})

        return wrapper

    return decorator


def add_page_info(qs, page, limit):
    max_page = 0
    try:
        paginator = Paginator(qs, limit)
        max_page = paginator.num_pages
        qs = paginator.page(page)
    except EmptyPage:
        qs = []
    return qs, max_page
