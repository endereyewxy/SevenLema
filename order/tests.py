from django.test import TestCase, RequestFactory, Client
from cmdb.models.user import User
from cmdb.models.shop import Shop
from cmdb.models.dish import Dish
from cmdb.models.order import Order
import json
from order.views import OrderCommitView


class OrderModelTests(TestCase):
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

        # serving shop has 1 2 3 4  dishes
        # no-serving shop has 2 3 4 5 dishes
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

    def test_parameter_lost(self):
        data = {
            'shop_id': self.shop_id,
            'dish_id': ['1'],
            # 'amount': 'test-amount',
            'addr': 'test-addr',
            'loc_lng': 'test-loc_lng',
            'loc_lat': 'test-loc_lat',
            'remarks': 'test-remarks',
        }
        resp = self.client.post('/order/new/', data=data)
        self.assertJSONEqual(resp.content, {'code': 101, 'msg': 'parameters lost'})

    def test_shop_no_exist(self):
        data = {
            'shop_id': '3',
            'dish_id': ['1'],
            'amount': 'test-amount',
            'addr': 'test-addr',
            'loc_lng': 'test-loc_lng',
            'loc_lat': 'test-loc_lat',
            'remarks': 'test-remarks',
        }
        resp = self.client.post('/order/new/', data=data)
        self.assertJSONEqual(resp.content, {'code': 106, 'msg': 'shop no exist'})

    def test_shop_no_serving(self):
        data = {
            'shop_id': self.no_serving_shop_id,
            'dish_id': ['1'],
            'amount': 'test-amount',
            'addr': 'test-addr',
            'loc_lng': 'test-loc_lng',
            'loc_lat': 'test-loc_lat',
            'remarks': 'test-remarks',
        }
        resp = self.client.post('/order/new/', data=data)
        self.assertJSONEqual(resp.content, {'code': 106, 'msg': 'shop no serving time'})

    # getting dish 5 from shop
    def test_dish_no_exist(self):
        data = {
            'shop_id': self.shop_id,
            'dish_id': ['1','7', '9'],
            'amount': 'test-amount',
            'addr': 'test-addr',
            'loc_lng': 'test-loc_lng',
            'loc_lat': 'test-loc_lat',
            'remarks': 'test-remarks',
        }
        resp = self.client.post('/order/new/', data=data)
        self.assertJSONEqual(resp.content, {'code': 106, 'msg': 'dish no exist'})

    # def test_dish_no_in_shop(self):
    #
    # def test_dish_no_in_stack(self):
