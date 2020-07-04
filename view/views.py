from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from cmdb.models.user import User


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
    ctx['shop_id'] = shop_id
    return render(request, 'dish.html', ctx)
