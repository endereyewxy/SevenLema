from django.forms import model_to_dict
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from cmdb.models.shop import Shop
from cmdb.models.user import User
from cmdb.models.order import Order


@require_GET
def root(request):
    return redirect('/index/')


@require_GET
def register(request):
    return render(request, 'register.html')


@require_GET
def login(request):
    if 'id' in request.session:
        return redirect('/')
    else:
        return render(request, 'login.html')


def get_login_context(request):
    if 'id' in request.session:
        ctx = {'login': True}
        ctx.update(model_to_dict(User.objects.get(id=request.session['id'])))
        return ctx
    else:
        return {'login': False}


@require_GET
def shop(request):
    return render(request, 'shop.html', get_login_context(request))


@require_GET
def dish(request, shop_id):
    ctx = get_login_context(request)
    try:
        shop_ = Shop.objects.get(id=shop_id)
        ctx['shop_obj'] = model_to_dict(shop_)
        ctx['is_admin'] = 'id' in request.session and shop_.user_id == request.session['id']
    except Shop.DoesNotExist:
        raise Http404('找不到商户')
    return render(request, 'dish.html', ctx)


@require_GET
def orders(request):
    ctx = get_login_context(request)
    if ctx['login']:
        return render(request, 'viewOrders.html', ctx)
    else:
        raise Http404('尚未登录')


@require_GET
def shop_info(request):
    ctx = get_login_context(request)
    if ctx['login']:
        return render(request, 'shopInfo.html', ctx)
    else:
        raise Http404('找不到商户')

