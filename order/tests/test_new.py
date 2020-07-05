from django.test import TestCase, RequestFactory, Client
from cmdb.models.user import User
from cmdb.models.shop import Shop
from cmdb.models.dish import Dish
from cmdb.models.order import Order
import json
import time
from datetime import datetime


class OrderModelTests(TestCase):
    # def _set_id_session(self, id="demo2"):
    #     """
    #     hack the session code to change it to the right one
    #     """
    #     from django.contrib.sessions.models import Session
    #     from django.contrib.sessions.backends.db import SessionStore
    #     session = Session.objects.get(pk=self.client.cookies['sessionid'].value)
    #     newsession = {"id": id}
    #     session.session_data = SessionStore().encode(newsession)
    #     session.save()

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
        user.save()
        self.user_id = str(user.id)
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

    def test_no_login(self):
        data = {
            'shop_id': self.shop_id,
            'dish_id': ['1'],
            'amount': 'test-amount',
            'addr': 'test-addr',
            'loc_lng': 'test-loc_lng',
            'loc_lat': 'test-loc_lat',
            'remarks': 'test-remarks',
        }

        obj = json.dumps(data)
        session = self.client.session
        del session['id']
        session.save()
        resp = self.client.post('/order/new/', data=obj, content_type='application/json')
        resjson = json.loads(resp.content)
        self.assertJSONEqual(resp.content, {'code': 103, 'msg': 'no login in '})

    def test_parameter_lost(self):
        data = {
            'shop_id': self.shop_id,
            'dish_id': ['1'],
            'amount': '',  # parameter lost
            'addr': 'test-addr',
            'loc_lng': 'test-loc_lng',
            'loc_lat': 'test-loc_lat',
            'remarks': 'test-remarks',
        }
        obj = json.dumps(data)
        resp = self.client.post('/order/new/', data=obj, content_type='application/json')
        resjson = json.loads(resp.content)
        self.assertJSONEqual(resp.content, {'code': 101, 'msg': 'parameters lost'})

    def test_shop_no_exist(self):
        data = {
            'shop_id': '3',  # shop no exist
            'dish_id': ['1'],
            'amount': 'test-amount',
            'addr': 'test-addr',
            'loc_lng': 'test-loc_lng',
            'loc_lat': 'test-loc_lat',
            'remarks': 'test-remarks',
        }
        obj = json.dumps(data)
        resp = self.client.post('/order/new/', data=obj, content_type='application/json')
        resjson = json.loads(resp.content)
        self.assertJSONEqual(resp.content, {'code': 106, 'msg': 'shop no exist'})

    def test_shop_no_serving(self):
        data = {
            'shop_id': self.no_serving_shop_id,  # shop no serving
            'dish_id': ['1'],
            'amount': 'test-amount',
            'addr': 'test-addr',
            'loc_lng': 'test-loc_lng',
            'loc_lat': 'test-loc_lat',
            'remarks': 'test-remarks',
        }
        obj = json.dumps(data)
        resp = self.client.post('/order/new/', data=obj, content_type='application/json')
        resjson = json.loads(resp.content)
        self.assertJSONEqual(resp.content, {'code': 106, 'msg': 'shop no serving time'})

    # getting dish 5 from shop
    def test_dish_no_exist(self):
        data = {
            'shop_id': self.shop_id,
            'dish_id': ['1', '3', '7', '9'],
            'amount': 'test-amount',
            'addr': 'test-addr',
            'loc_lng': 'test-loc_lng',
            'loc_lat': 'test-loc_lat',
            'remarks': 'test-remarks',
        }
        obj = json.dumps(data)
        resp = self.client.post('/order/new/', data=obj, content_type='application/json')
        resjson = json.loads(resp.content)
        self.assertJSONEqual(resjson,
                             '{"106": ["dish 1 not on sale", "dish 3 not on sale"], "105": ["dish 7 not in the shop 1", "dish 9 not in the shop 1"]}')

    def test_commit_success(self):
        data = {
            'shop_id': self.shop_id,
            'dish_id': ['0', '2'],
            'amount': ['2', '3'],
            'addr': 'test-addr',
            'loc_lng': 1,
            'loc_lat': 1,
            'remarks': 'test-remarks',
        }
        obj = json.dumps(data)
        resp = self.client.post('/order/new/', data=obj, content_type='application/json')
        resjson = json.loads(resp.content)
        order_id = int(time.time())
        self.assertJSONEqual(resp.content, {'code': 0, 'msg': 'creating order succeed', 'data': 1})
