from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from cmdb.models.shop import Shop
from cmdb.models.user import User


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


@require_GET
def shop(request):
    user = User.objects.get(id=1)
    return render(request, 'shop.html', model_to_dict(user))


@require_GET
def dish(request, shop_id):
    user = User.objects.get(id=1)
    ctx = model_to_dict(user)
    shop_ = Shop.objects.get(id=shop_id)
    ctx['shop_obj'] = model_to_dict(shop_)
    return render(request, 'dish.html', ctx)
