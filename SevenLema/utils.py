import os
from hashlib import md5
from uuid import uuid4

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse

from cmdb.models.user import User


def check_login_status(request):
    if 'id' in request.session:
        try:
            return True, User.objects.get(id=request.session['id'])
        except User.DoesNotExist:
            pass
    return False, JsonResponse({'code': 103, 'msg': '用户尚未登录'})


def upload_image(image):
    if image.size > 20480000:
        return False, JsonResponse({'code': 105, 'msg': '图片体积过大'})
    ext = image.name.split('.')[-1]
    if ext not in ['svg', 'jpg', 'png']:
        return False, JsonResponse({'code': 101, 'msg': '图片格式不支持'})
    tok = md5(str(uuid4()).encode('utf-8')).hexdigest()
    with open(os.path.join(settings.STATIC_ROOT, 'images', tok + '.' + ext), 'wb') as f:
        for chunk in image.chunks():
            f.write(chunk)
    return True, tok + '.' + ext


def add_page_info(qs, page, limit):
    max_page = 0
    try:
        paginator = Paginator(qs, limit)
        max_page  = paginator.num_pages
        qs        = paginator.page(page)
    except EmptyPage:
        qs        = []
    return qs, max_page
