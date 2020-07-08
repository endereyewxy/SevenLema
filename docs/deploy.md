# 部署注意事项

- 修改setting.py中，设置`DEBUG=False`，`ALLOWED_HOSTS = ['服务器的IP或域名']`
- 部署美团爬虫数据步骤：
    1. 删除db.sqlite3（如果有的话）
    2. 执行`python manage.py migrate`
    3. 执行`python spider/generate_sql.py`
    4. 向db.sqlite3中写入spider/spider.sql
    5. 执行`python spider/download_images/py`