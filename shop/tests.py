# Developer: endereye <endereyewxy@gmail.com>

import json

from django.test import TestCase, RequestFactory

from cmdb.models.shop import Shop
from cmdb.models.user import User
from search.views import shop


class ShopCreateTestCase(TestCase):
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
        wrong_shop = Shop.objects.create(
            user=wrong_user,
            name='test-name',
            image='9441c87f9df8954b',
            desc='A Simple Description',
            addr='test-addr',
            loc_lng=0,
            loc_lat=0,
            phone='10394719283',
            serving=True
        )
        wrong_shop.save()
        self.wrong_shop_id = wrong_shop.id
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
        self.shop_id = shop.id
        session = self.client.session
        session['id'] = user.id
        session.save()

    def test_create(self):
        data = {
            'name': 'test-name',
            'image': 'test-image',
            'desc': 'description',
            'addr': 'test-addr',
            'loc_lng': 114.85975,
            'loc_lat': 30.42604,
            'avg_price': 50,
            'phone': '10394719283',
        }
        resp = self.client.post('/shop/create/', data=data)
        self.assertEqual(json.loads(resp.content)['code'], 0)

    def test_edit(self):
        data = {
            'shop_id': self.shop_id,
            'name': 'edit-name',
            'avg_price': 200,
        }
        resp = self.client.post('/shop/edit/', data=data)
        self.assertEqual(json.loads(resp.content)['code'], 0)
        shop = Shop.objects.get(id=self.shop_id)
        self.assertEqual([shop.name, shop.avg_price], ['edit-name', 200])

    def test_shop_no_in_user(self):
        data = {
            'shop_id': self.wrong_shop_id,
            'name': 'edit-name',
            'avg_price': 200,
        }
        resp = self.client.post('/shop/edit/', data=data)
        self.assertEqual(json.loads(resp.content)['code'], 102)
