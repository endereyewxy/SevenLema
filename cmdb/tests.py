from django.test import TestCase

from .models.order import Order
from .models.shop import Shop
from .models.user import User


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test-username',
            password='9441c87f9df8954b',
            salt='test-salt',
            addr='test-addr',
            loc_lng=0,
            loc_lat=0,
            phone='10394719283'
        )
        self.shop = Shop.objects.create(
            user=self.user,
            name='test-name',
            image='9441c87f9df8954b',
            desc='A Simple Description',
            addr='test-addr',
            loc_lng=0,
            loc_lat=0,
            phone='10394719283',
            serving=True
        )
        self.order = Order.objects.create(
            user=self.user,
            shop=self.shop,
            remarks='',
            addr='test-addr',
            loc_lng=0,
            loc_lat=0,
            tm_ordered=0
        )

    def test_user_check_password(self):
        self.assert_(self.user.check_password('test-password'))

    def test_user_set_password(self):
        self.user.set_password('test-password')
        self.assertEqual(self.user.password, '9441c87f9df8954b')

    def test_shop_default(self):
        self.assertEqual(self.shop.avg_price, 0)
        self.assertEqual(self.shop.sales, 0)

    def test_order_foreign_key(self):
        self.assertEqual(self.order.user_id, self.user.id)
        self.assertEqual(self.order.shop_id, self.shop.id)
