import json

if __name__ == '__main__':
    with open('spider.json', 'r') as f:
        data = json.load(f)
    images = []
    with open('spider.sql', 'w') as f:
        user_id, shop_id, dish_id = 0, 0, 0
        for shop in data:
            if shop_id % 5 == 0:
                user_id += 1
                f.write(
                    f"INSERT INTO cmdb_user"
                    f"(username, password, salt, addr, loc_lng, loc_lat, phone)"
                    f"VALUES"
                    f"('美团外卖{user_id}', 'f7eb3d1b66527f563e9510d7561dd4fc', 'iednycl8j2q1ou3stzb57r4xm60vh9kg', '-', 106.52031,"
                    f"29.53899, '00000000000');\n"
                )
            f.write(
                f"INSERT INTO cmdb_shop"
                f"(name, image, desc, addr, loc_lng, loc_lat, avg_price, sales, phone, serving, user_id)"
                f"VALUES"
                f"('{shop['name']}', '{shop['image'][-36:]}', '美团外卖', '{shop['addr']}', {shop['loc_lng']},"
                f"{shop['loc_lat']}, {shop['avg_price']}, 0, '{shop['phone']}', true, {user_id});\n"
            )
            images.append(shop['image'])
            shop_id += 1
            for dish in shop['dishes']:
                f.write(
                    f"INSERT INTO cmdb_dish"
                    f"(name, image, desc, price, sales, serving, shop_id)"
                    f"VALUES"
                    f"('{dish['name']}', '{dish['image'][-36:]}', '美团外卖', {dish['price']}, 0, true, {shop_id});\n"
                )
                images.append(dish['image'])
                dish_id += 1
    with open('images.json', 'w') as f:
        json.dump(images, f)
