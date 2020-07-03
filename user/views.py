from django.shortcuts import render, redirect
from django.http import JsonResponse
from user import models
from django.db.models import Max

database = models.user.objects.all()


# Create your views here.
def signUpPage(request):

    database_phone = database.values('phone')

    database_maxId = database.aggregate(Max('userId'))

    # print(database)

    if request.POST:
        # 获取用户信息
        username = request.POST.get('username', None)
        phone = request.POST.get('phone', None)
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)

        if password1 != password2:
            return JsonResponse(
                {
                    'code': 105,
                    'msg': '两次输入密码不一致，清重新输入',

                })

        elif len(phone) != 11:
            return JsonResponse(
                {
                    'code': 105,
                    'msg': '手机号格式输入有误，请重新输入',

                })

        elif phone in database_phone:  # 数据库
            return JsonResponse(
                {
                    'code': 104,
                    'msg': '手机号已被注册，清重新输入',
                })

        else:
            newUser = {
                'username': username,
                'password': password1,
                'phone': phone
            }

            models.user.objects.create(
                username=username,
                userId=int(database_maxId) + 1,
                phone=phone,
                password=password1
            )

            return JsonResponse({
                'code': 0,
                'msg': '注册用户成功',
                'data': newUser
            })


    else:

        return render(request, 'signUpPage.html')


def gotoLogin(request):
    return redirect('/login')


def login(request):

    if request.POST:
        # 获取用户信息
        account = request.POST.get('account', None)
        password = request.POST.get('password', None)

