from django.forms import model_to_dict
from django.shortcuts import render
from django.views.decorators.http import require_GET

from cmdb.models.user import User


@require_GET
def shop(request):
    user = User.objects.get(id=1)
    return render(request, 'shop.html', model_to_dict(user))
