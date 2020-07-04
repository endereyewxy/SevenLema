from django.shortcuts import render, redirect
from django.http import JsonResponse
# from user import models
from django.db.models import Max
from cmdb.models.user import User

# database = models.ser.objects.all()
database = User.objects.all()


# Create your views here.
def signUpPage(request):
    database_phone = database.values('phone')
    #
    # database_maxId = database.aggregate(Max('userId'))

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

            database.create(
                username=username,
                # userId=int(database_maxId) + 1,
                phone=phone,
                password=password1
            )

            return JsonResponse({
                'code': 0,
                'msg': '注册用户成功',
                'data': newUser
            })


    else:

        return JsonResponse({
            'code': 101,
            'msg': '请求错误',
        })


def gotoLogin(request):
    # return redirect('/login')
    pass


def login(request):
    if request.POST:
        # 获取用户信息
        username = request.POST.get('username', None)
        phone = request.POST.get('phone', None)

        password = request.POST.get('password', None)

        login_usn = User.objects.filter(username=username)
        login_pho = User.objects.filter(phone=phone)

        usn = login_usn.all()

        if login_usn.exists():

            for us in usn:

                if us.password == password:
                    return JsonResponse({
                        'code': 0,
                        'msg': '登录成功'
                    })

            # user = login_usn.first()

            # if user.password == password:
            #
            #     return JsonResponse({
            #         'code':0,
            #         'msg':'登录成功'
            #     })

        elif login_pho.exists():

            pho = login_pho.first()

            if pho.password == password:
                return JsonResponse({
                    'code': 0,
                    'msg': '登录成功'
                })

        else:
            return JsonResponse({
                'code': 102,
                'msg': '用户不存在'
            })

    else:

        return JsonResponse({
            'code': 101,
            'msg': '请求错误',
        })
