# 数据表说明

- 所有时间相关字段均为UNIX时间戳。

## user

用于存储用户相关信息。

| 字段     | 类型         | 说明     | 是否必须 | 备注                |
| -------- | ------------ | -------- | -------- | ------------------- |
| id       | INTEGER      |          | 是       | 主键，自增          |
| username | VARCHAR(20)  | 用户名   | 是       |                     |
| password | CHAR(32)     | 密码     | 是       | 密码加盐之后的MD5值 |
| salt     | CHAR(32)     | 盐       | 是       |                     |
| addr     | VARCHAR(50)  | 地址     | 否       |                     |
| loc_lng  | DECIMAL(9,5) | 位置经度 | 否       |                     |
| loc_lat  | DECIMAL(9,5) | 位置纬度 | 否       |                     |
| phone    | CHAR(11)     | 电话号码 | 是       |                     |

## shop

用于存储商户相关信息。

| 字段      | 类型         | 说明       | 是否必须 | 备注                       |
| --------- | ------------ | ---------- | -------- | -------------------------- |
| id        | INTEGER      |            | 是       | 主键，自增                 |
| user_id   | INTEGER      | 所属用户ID | 是       | 表user的外键               |
| name      | VARCHAR(50)  | 名称       | 是       |                            |
| image     | CHAR(36)     | 图片       | 是       | static目录下的文件名，包括扩展名 |
| desc      | TEXT         | 描述       | 是       |                            |
| addr      | VARCHAR(50)  | 地址       | 是       |                            |
| loc_lng   | DECIMAL(9,5) | 位置经度   | 是       |                            |
| loc_lat   | DECIMAL(9,5) | 位置纬度   | 是       |                            |
| avg_price | INTEGER      | 人均消费   | 是       | 单位为分（除100为RMB价格） |
| sales     | INTEGER      | 销量       | 是       | 订单总数量                 |
| phone     | CHAR(11)     | 电话号码   | 否       |                            |
| serving   | BOOLEAN      | 是否营业   | 是       |                            |

## dish

用于存储菜品相关信息。

| 字段    | 类型        | 说明       | 是否必须 | 备注                       |
| ------- | ----------- | ---------- | -------- | -------------------------- |
| id      | INTEGER     |            | 是       | 主键，自增                 |
| shop_id | INTEGER     | 所属商户ID | 是       | 表shop的外键               |
| name    | VARCHAR(50) | 名称       | 是       |                            |
| image   | CHAR(36)    | 图片       | 是       | static目录下的文件名，包括扩展名 | |
| desc    | TEXT        | 描述       | 是       |                            |
| price   | INTEGER     | 单价       | 是       | 单位为分（除100为RMB价格） |
| sales   | INTEGER     | 销量       | 是       |                            |
| serving | BOOLEAN     | 是否有货   | 是       |                            |

## order

用于存储订单相关信息。

| 字段        | 类型         | 说明       | 是否必须 | 备注                   |
| ----------- | ------------ | ---------- | -------- | ---------------------- |
| id          | INTEGER      |            | 是       | 主键，自增             |
| user_id     | INTEGER      | 下单用户ID | 是       | 表user的外键           |
| shop_id     | INTEGER      | 处理商户ID | 是       | 表shop的外键           |
| remarks     | VARCHAR(50)  | 备注       | 是       |                        |
| addr        | VARCHAR(50)  | 地址       | 是       |                        |
| loc_lng     | DECIMAL(9,5) | 位置经度   | 是       |                        |
| loc_lat     | DECIMAL(9,5) | 位置纬度   | 是       |                        |
| tm_ordered  | LONG INTEGER | 下单时间   | 是       |                        |
| tm_finished | LONG INTEGER | 送达时间   | 否       | `null`表示订单尚未完成 |

## dish_order

用于存储订单和菜品关系的相关信息。

| 字段     | 类型    | 说明             | 是否必须 | 备注          |
| -------- | ------- | ---------------- | -------- | ------------- |
| dish_id  | INTEGER | 菜品ID           | 是       | 表dish的外键  |
| order_id | INTEGER | 订单ID           | 是       | 表order的外键 |
| amount   | INTEGER | 订单中该菜品数量 | 是       | 大于零        |

注：该表主键为dish_id和order_id。

## tag

用于存储商户标签的相关信息。

| 字段 | 类型        | 说明 | 是否必须 | 备注       |
| ---- | ----------- | ---- | -------- | ---------- |
| id   | INTEGER     |      | 是       | 主键，自增 |
| tag  | VARCHAR(20) | 标签 | 是       |            |

## tag_shop

用于存储标签和商户的对应关系。

| 字段    | 类型    | 说明   | 是否必须 | 备注         |
| ------- | ------- | ------ | -------- | ------------ |
| shop_id | INTEGER | 商户ID | 是       | 表shop的外键 |
| tag_id  | INTEGER | 标签ID | 是       | 表tag的外键  |

注：该表主键为shop_id和tag_id。
