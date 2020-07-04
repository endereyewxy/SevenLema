from django.test import TestCase, RequestFactory, Client
from cmdb.models.user import User
from cmdb.models.shop import Shop
from cmdb.models.dish import Dish
from cmdb.models.order import Order
import json
import time
from datetime import datetime


class OrderModelTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        session = self.client.session

        user = User.objects.create(
            username='test-username',
            password='9441c87f9df8954b',
            salt='test-salt',
            addr='test-addr',
            loc_lng=0,
            loc_lat=0,
            phone='10394719283'
        )
        wrong_user = User.objects.create(
            username='wrong-username',
            password='9441c87f9df8954b',
            salt='test-salt',
            addr='test-addr',
            loc_lng=0,
            loc_lat=0,
            phone='10394719283'
        )
        wrong_user.save()
        user.save()
        self.user_id = str(user.id)
        self.wrong_id = str(wrong_user.id)
        session['id'] = user.id
        session.save()

        shop = Shop.objects.create(
            user_id=user,
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

        no_serving_shop = Shop.objects.create(
            user_id=user,
            name='test-name',
            image='9441c87f9df8954b',
            desc='A Simple Description',
            addr='test-addr',
            loc_lng=0,
            loc_lat=0,
            phone='10394719283',
            serving=False
        )
        no_serving_shop.save()
        self.no_serving_shop_id = str(no_serving_shop.id)

        # serving shop has  0 1 2 3   dishes
        # no-serving shop has 1 2 3 4  dishes
        for i in range(4):
            Dish.objects.create(
                shop_id=shop,
                name=str(i),
                image='0123456789abcdef',
                desc='',
                price=i,
                sales=i,
                serving=i % 2 == 0
            ).save()
            Dish.objects.create(
                shop_id=no_serving_shop,
                name=str(i + 1),
                image='0123456789abcdef',
                desc='',
                price=i,
                sales=i,
                serving=i % 2 == 0
            ).save()

    def test_get_info_success_user(self):
        data = {
            'shop_id': self.shop_id,
            'dish_id': ['2'],
            'amount': ['2'],
            'addr': 'test-addr',
            'loc_lng': 1,
            'loc_lat': 1,
            'remarks': 'test-remarks',
        }
        obj = json.dumps(data)
        tm_ordered = int(time.time())
        resp = self.client.post('/order/new/', data=obj, content_type='application/json')
        resjson = json.loads(resp.content)
        self.assertJSONEqual(resp.content, {'code': 0, 'msg': 'creating order succeed', 'data': 1})

        data2 = {
            'order_id': 1,
            'shop_id': self.shop_id,
            'page': 1,
            'limit': 5,
            'unfinished': False
        }
        obj2 = json.dumps(data2)
        resp2 = self.client.post('/order/info/', data=obj2, content_type='application/json')
        resjson = json.loads(resp2.content)

        self.assertJSONEqual(resp2.content,
                             {"code": 0, "msg": "get order info succeed",
                              "data": [{"user_id": 1}, {"user_name": "test-username"}, {"user_id": "10394719283"},
                                       {"shop_id": 1}, {"shop_name": "test-name"},
                                       {"dish_id": 5, "name": "2", "amount": 2}, {"loc_lng": "0"}, {"loc_lat": "0"},
                                       {"remarks": "test-remarks"}, {"tm_ordered": tm_ordered}, {"tm_finished": 0}]})

    def test_get_info_success_shop(self):
        data = {
            'shop_id': self.shop_id,
            'dish_id': ['2'],
            'amount': ['2'],
            'addr': 'test-addr',
            'loc_lng': 1,
            'loc_lat': 1,
            'remarks': 'test-remarks',
        }
        obj = json.dumps(data)
        tm_ordered = int(time.time())
        resp = self.client.post('/order/new/', data=obj, content_type='application/json')
        resjson = json.loads(resp.content)
        self.assertJSONEqual(resp.content, {'code': 0, 'msg': 'creating order succeed', 'data': 1})
        data2 = {
            'shop_id': self.shop_id,
            'page': 1,
            'limit': 5,
            'unfinished': False
        }
        obj2 = json.dumps(data2)
        resp2 = self.client.post('/order/info/', data=obj2, content_type='application/json')
        resjson = json.loads(resp2.content)

        self.assertJSONEqual(resp2.content,
                             {"code": 0, "msg": "get order info succeed",
                              "data": [{"user_id": 1}, {"user_name": "test-username"}, {"user_id": "10394719283"},
                                       {"shop_id": 1}, {"shop_name": "test-name"},
                                       {"dish_id": 5, "name": "2", "amount": 2}, {"loc_lng": "0"}, {"loc_lat": "0"},
                                       {"remarks": "test-remarks"}, {"tm_ordered": tm_ordered}, {"tm_finished": 0}]})

    def test_no_user_order_input(self):
        data = {
            'shop_id': self.shop_id,
            'dish_id': ['2'],
            'amount': ['2'],
            'addr': 'test-addr',
            'loc_lng': 1,
            'loc_lat': 1,
            'remarks': 'test-remarks',
        }
        obj = json.dumps(data)
        tm_ordered = int(time.time())
        resp = self.client.post('/order/new/', data=obj, content_type='application/json')
        resjson = json.loads(resp.content)
        self.assertJSONEqual(resp.content, {'code': 0, 'msg': 'creating order succeed', 'data': 1})
        data2 = {
            'page': 1,
            'limit': 5,
            'unfinished': False
        }
        obj2 = json.dumps(data2)
        resp2 = self.client.post('/order/info/', data=obj2, content_type='application/json')
        resjson = json.loads(resp2.content)

        self.assertJSONEqual(resp2.content,
                             {'code': 103, 'msg': "no order_id and shop_id input "})
