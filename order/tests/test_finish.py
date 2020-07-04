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

        order = Order.objects.create(
            user_id=user,
            shop_id=shop,
            remarks='remarks',
            addr='addr',
            loc_lng=1,
            loc_lat=1,
            tm_ordered=int(time.time()),
            tm_finished=False
        )
        order.save()
        self.order = order

        wrong_order = Order.objects.create(
            user_id=wrong_user,
            shop_id=shop,
            remarks='remarks',
            addr='addr',
            loc_lng=1,
            loc_lat=1,
            tm_ordered=int(time.time()),
            tm_finished=False
        )
        wrong_user.save()
        self.wrong_order = wrong_order

    def test_no_user_connection(self):
        data = {
            'order_id': self.wrong_order.id,
        }
        obj = json.dumps(data)
        resp = self.client.post('/order/finish/', data=obj, content_type='application/json')
        self.assertJSONEqual(resp.content, {'code': 103, 'msg': 'order not belong to this user '})

    def test_not_finish(self):
        data = {
            'order_id': self.order.id,
        }
        obj = json.dumps(data)
        resp = self.client.post('/order/finish/', data=obj, content_type='application/json')
        self.assertJSONEqual(resp.content, {'code': 105, 'msg': 'order not finish now'})
