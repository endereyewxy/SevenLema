# 重要！！！

### 关于验证用户登录状态

如果用户已经登录，他的ID会被保存在`session['id']`里，例如

```python
if 'id' in session:                           # 如果已经登录
    user = User.objects.get(id=session['id']) # 获取用户信息
else:
    pass
```

### 关于数据库

所有的model都在cmdb下面，**不需要自己去实现**。

### 关于前端CSRF

前端的HTML里要加`{% csrf_token %}`，AJAX请求要加csrf参数。