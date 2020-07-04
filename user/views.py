from django.shortcuts import render, redirect
from django.http import JsonResponse
# from user import models
from django.db.models import Max
from cmdb.models.user import User

# database = models.ser.objects.all()
database = User.objects.all()


# Create your views here.
def signUpPage(request):

    if request.POST:
        # 获取用户信息
        username = request.POST.get('username', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password1', None)

        # else:
        newUser = {
            'username': username,
            'password': password,
            'phone': phone
        }

        database.create(
            username=username,
            # userId=int(database_maxId) + 1,
            phone=phone,
            password=password
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


# def gotoLogin(request):
#     # return redirect('/login')
#     pass
#
#
# def login(request):
#     if request.POST:
#         # 获取用户信息
#         username = request.POST.get('username', None)
#         phone = request.POST.get('phone', None)
#
#         password = request.POST.get('password', None)
#
#         login_usn = User.objects.filter(username=username)
#         login_pho = User.objects.filter(phone=phone)
#
#         usn = login_usn.all()
#
#         if login_usn.exists():
#
#             for us in usn:
#
#                 if us.password == password:
#                     return JsonResponse({
#                         'code': 0,
#                         'msg': '登录成功'
#                     })
#
#             # user = login_usn.first()
#
#             # if user.password == password:
#             #
#             #     return JsonResponse({
#             #         'code':0,
#             #         'msg':'登录成功'
#             #     })
#
#         elif login_pho.exists():
#
#             pho = login_pho.first()
#
#             if pho.password == password:
#                 return JsonResponse({
#                     'code': 0,
#                     'msg': '登录成功'
#                 })
#
#         else:
#             return JsonResponse({
#                 'code': 102,
#                 'msg': '用户不存在'
#             })
#
#     else:
#
#         return JsonResponse({
#             'code': 101,
#             'msg': '请求错误',
#         })
