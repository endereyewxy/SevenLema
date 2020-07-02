# 功能需求

**粗体的**优先搞

正体的不着急

*斜体的*先放放

<span style="color:red;">红色的</span>做不出来



- 用户
  - **注册**
  - **登录**
  - **登出**
  - **搜索商户**
    - **按距离排序**
    - **按人均消费排序**
    - **按销量排序**
    - <span style="color:red;">配送范围限制</span>
    - *标签筛选*
  - **搜索菜品**
    - **按价格排序**
    - **按销量排序**
  - **下达订单**
  - **查看订单**
  - <span style="color:red;">取消订单</span>
- 商户
  - 创建
  - 修改商户信息
  - 添加、修改、删除菜品
  - 设置是否营业
  - 查看订单
  - 设置订单送达时间

# 模块设计

分若干模块（app）：

| app名称 | 说明     | 功能                                                         |
| ------- | -------- | ------------------------------------------------------------ |
| user    | 用户管理 | 用户注册、登录、登出API                                      |
| view    | 界面展现 | 展现给用户的界面，**不涉及任何业务逻辑**，仅包含简单的数据库查询 |
| shop    | 商户管理 | 创建商户、修改信息、设置是否营业                             |
| dish    | 菜品管理 | 添加、修改、删除菜品                                         |
| order   | 订单管理 | 下达订单，查看订单（买家和商户），设置订单送达时间（商户）   |
| search  | 搜索处理 | 处理搜索（商户，菜品）请求                                   |

除了view模块之外，其它模块均不涉及前端，所有请求返回JSON，格式为：

```json
{
    code: 0,   // 错误码，0表示无错误
    msg: "",   // 错误信息
    data: ...  // 返回数据
}
```

## user

### 用户注册

请求地址：/user/register

请求方法：POST

| 请求参数 | 类型   | 是否必须 | 说明     | 备注     |
| -------- | ------ | -------- | -------- | -------- |
| username | STRING | 是       | 用户名   |          |
| password | STRING | 是       | 密码     | 明文传输 |
| addr     | STRING | 否       | 地址     |          |
| loc_lng  | FLOAT  | 否       | 位置经度 |          |
| loc_lat  | FLOAT  | 否       | 位置纬度 |          |
| phone    | STRING | 是       | 电话号码 |          |

返回数据：无

注册成功后用户自动登录，在session中设置用户ID。

### 用户登录

请求地址：/user/login

请求方法：POST

| 请求参数 | 类型   | 是否必须 | 说明   | 备注     |
| -------- | ------ | -------- | ------ | -------- |
| username | STRING | 是       | 用户名 |          |
| password | STRING | 是       | 密码   | 明文传输 |

返回数据：无

用户登录成功后，在session中设置用户ID。

### 用户登出

请求地址：/user/logout

请求方法：POST

没有参数和返回数据，但销毁session。

## view

TODO 我搞不来，前端搞

## shop

TODO 暂缓

## dish

TODO 暂缓

## order

### 下达订单

请求地址：/order/new

请求方法：POST

| 请求参数 | 类型    | 是否必须 | 说明     | 备注               |
| -------- | ------- | -------- | -------- | ------------------ |
| shop_id  | INTEGER | 是       | 商户ID   |                    |
| dish_id  | INTEGER | 是       | 菜品ID   | 数组，属于给定商户 |
| amount   | INTEGER | 是       | 数量     | 数组，大于0        |
| addr     | STRING  | 是       | 地址     |                    |
| loc_lng  | FLOAT   | 是       | 位置经度 |                    |
| loc_lat  | FLOAT   | 是       | 位置纬度 |                    |
| remarks  | STRING  | 是       | 订单备注 |                    |

返回数据：

| 字段     | 类型    | 说明   | 备注 |
| -------- | ------- | ------ | ---- |
| order_id | INTEGER | 订单ID |      |

服务器校验：

- 用户已登录
- 所有菜品均有货
- 商户正在营业

### 查看订单

请求地址：/order/info

请求方法：GET

| 请求参数   | 类型    | 是否必须 | 说明                 | 备注                                         |
| ---------- | ------- | -------- | -------------------- | -------------------------------------------- |
| order_id   | INTEGER | 否       | 订单ID               | 不提供则返回所有和该用户（或商户）相关的订单 |
| shop_id    | INTEGER | 否       | 商户ID               | 不提供则为用户视角，提供则为商家视角         |
| page       | INTEGER | 是       | 页码                 | 从1开始                                      |
| limit      | INTEGER | 是       | 每页数量限制         |                                              |
| unfinished | BOOLEAN | 否       | 是否只返回未完成订单 | 默认为`False`                                |

返回数据为一个数组，数组中的每个对象包含以下字段：

| 字段        | 类型    | 说明         | 备注                     |
| ----------- | ------- | ------------ | ------------------------ |
| user_id     | INTEGER | 下单用户ID   |                          |
| username    | STRING  | 下单用户名   |                          |
| phone       | STRING  | 用户电话号码 |                          |
| shop_id     | INTEGER | 商户ID       |                          |
| shop_name   | STRING  | 商户名称     |                          |
| dishes      | ARRAY   | 所购菜品     | 对象数组                 |
| addr        | STRING  | 送达地址     |                          |
| loc_lng     | FLOAT   | 送达位置经度 |                          |
| loc_lat     | FLOAT   | 送达位置纬度 |                          |
| remarks     | STRING  | 订单备注     |                          |
| tm_ordered  | LONG    | 下单时间     |                          |
| tm_finished | LONG    | 送达时间     | 可能为`null`，表示未送达 |

其中dishes字段是一个数组，数组中每个对象包含以下字段：

| 字段    | 类型    | 说明     | 备注 |
| ------- | ------- | -------- | ---- |
| dish_id | INTEGER | 菜品ID   |      |
| name    | STRING  | 菜品名称 |      |
| amount  | INTEGER | 数量     |      |

服务器校验：

- 如果提供order_id，则必须与该用户（或商户）相关。
- 如果提供shop_id，则必须与该用户相关。

### 设置订单送达

请求地址：/order/finish

请求方法：POST

| 请求参数 | 类型    | 是否必须 | 说明     | 备注               |
| -------- | ------- | ------ | ---- | ---- |
| order_id | INTEGER | 是 | 订单ID ||

返回数据：无

服务器校验：

- order_id必须与该用户下辖的某个商户相关。
- 该订单必须尚未送达。

## search

## 搜索商户

请求地址：/search/shop

请求方法：GET

| 请求参数 | 类型    | 是否必须 | 说明                   | 备注           |
| -------- | ------- | -------- | ---------------------- | -------------- |
| name     | STRING  | 是       | 名字                   | 搜索相似的名字 |
| order    | STRING  | 是       | 排序方式               |                |
| tags     | STRING  | 否       | 筛选的标签             | 数组           |
| page     | INTEGER | 是       | 页码                   | 从1开始        |
| limit    | INTEGER | 是       | 每页数量限制           |                |
| serving  | BOOLEAN | 否       | 是否只返回营业中的商户 |                |

order的可能取值：

- `dist`：按距离从近到远排序
- `avg_price`：按人均消费从低到高排序
- `sales`：按销量从高到低排序

返回数据是一个数组，数组中每个对象都包含如下字段：

| 字段      | 类型    | 说明     | 备注                   |
| --------- | ------- | -------- | ---------------------- |
| shop_id   | INTEGER | 商户ID   |                        |
| name      | STRING  | 商户名称 |                        |
| image     | STRING  | 图片     | static目录下的文件名   |
| desc      | STRING  | 描述     |                        |
| addr      | STRING  | 地址     |                        |
| loc_lng   | FLOAT   | 位置经度 |                        |
| loc_lat   | FLOAT   | 位置纬度 |                        |
| dist      | FLOAT   | 距离     | 单位：米               |
| avg_price | FLOAT   | 人均消费 | 单位：元（**不是分**） |
| sales     | INTEGER | 销量     |                        |
| phone     | STRING  | 电话号码 |                        |
| serving   | BOOLEAN | 是否营业 |                        |

## 搜索菜品

请求地址：/search/dish

请求方法：GET

| 请求参数 | 类型    | 是否必须 | 说明                 | 备注                   |
| -------- | ------- | -------- | -------------------- | ---------------------- |
| shop_id  | INTEGER | 是       | 商户ID               | 仅搜索该商户提供的菜品 |
| name     | STRING  | 是       | 名字                 | 搜索相似的名字         |
| page     | INTEGER | 是       | 页码                 | 从1开始                |
| limit    | INTEGER | 是       | 每页数量限制         |                        |
| serving  | BOOLEAN | 否       | 是否只返回有货的菜品 |                        |

返回数据是一个数组，数组中每个对象都包含如下字段：

| 字段    | 类型    | 说明     | 备注                   |
| ------- | ------- | -------- | ---------------------- |
| dish_id | INTEGER | 菜品ID   |                        |
| name    | STRING  | 菜品名称 |                        |
| image   | STRING  | 图片     | static目录下的文件名   |
| desc    | STRING  | 描述     |                        |
| price   | FLOAT   | 单价     | 单位：元（**不是分**） |
| sales   | INTEGER | 销量     |                        |
| serving | BOOLEAN | 是否营业 |                        |