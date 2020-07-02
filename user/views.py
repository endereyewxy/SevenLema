from django.shortcuts import render, redirect


# Create your views here.
def signUpPage(request):
    if request.POST:
        # 获取用户信息
        mailbox = request.POST.get('mailbox', None)
        account = request.POST.get('account', None)
        password1 = request.POST.get('password', None)
        password2 = request.POST.get()

        # 模拟判断用户是否存在与数据库
        if mailbox == 'siri' and password == '123':
            # 登陆成功

            # 把内容存入cookie
            resp = redirect('/app01/home/')

            # 设置cookie
            resp.set_signed_cookie('account', account, salt='llxnb')

            # 把数据存入session
            request.session['account'] = account

            # 响应到客户端
            return resp

        else:
            # 账号密码不对时
            return render(request, 'signUpPage.html',
                          {'msg': '账号或密码有误，请检查后登录'})

    # 为GET请求时，响应到客户端
    else:

        # 获取到cookie的值
        account = request.get_signed_cookie('account', None, salt='llxnb')

        # 判断account是否存在
        if account:
            # 存在，则自动写入到输入框
            return render(request, 'signUpPage.html', {'account': account})
        else:
            # account不存在
            return render(request, 'signUpPage.html')


def gotoLogin(request):

    return redirect('/login/')