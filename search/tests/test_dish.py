# Developer: endereye <endereyewxy@gmail.com>

import json

from django.test import TestCase, RequestFactory

from cmdb.models.dish import Dish
from cmdb.models.shop import Shop
from cmdb.models.user import User
from search.views import dish


class SearchDishTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        user = User.objects.create(
            username='test-username',
            password='9441c87f9df8954b',
            salt='test-salt',
            addr='test-addr',
            loc_lng=0,
            loc_lat=0,
            phone='10394719283'
        )
        user.save()
        shop = Shop.objects.create(
            user=user,
            name='test-name',
            image='9441c87f9df8954b',
            desc='A Simple Description',
            addr='test-addr',
            loc_lng=0,
            loc_lat=0,
            phone='10394719283',
            serving=True
        )
        shop.save()
        self.shop_id = str(shop.id)

        for i in range(4):
            Dish.objects.create(
                shop=shop,
                name=str(i),
                image='0123456789abcdef',
                desc='',
                price=i,
                sales=i,
                serving=i % 2 == 0
            ).save()

    def test_order_price(self):
        resp = dish(self.factory.get('/search/dish?shop_id=' + self.shop_id + '&name=&order=price&page=1&limit=20'))
        self.assertEqual([int(obj['name']) for obj in json.loads(resp.content)['data']], [0, 1, 2, 3])

    def test_order_sales(self):
        resp = dish(self.factory.get('/search/dish?shop_id=' + self.shop_id + '&name=&order=sales&page=1&limit=20'))
        self.assertEqual([int(obj['name']) for obj in json.loads(resp.content)['data']], [3, 2, 1, 0])