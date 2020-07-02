import json

from django.test import TestCase, RequestFactory

from cmdb.models import User, Shop
from search.views import shop


class SearchShopTestCase(TestCase):
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

        loc_lng = [114.85975, 115.99004, 114.31592, 114.32159]
        loc_lat = [30.42604, 29.71414, 29.83217, 30.52886]
        for i in range(4):
            Shop.objects.create(
                user=user,
                name=str(i),
                image='0123456789abcdef',
                desc='',
                addr='',
                loc_lng=loc_lng[i],
                loc_lat=loc_lat[i],
                avg_price=i,
                sales=i,
                phone='10928374657',
                serving=i % 2 == 0
            ).save()

    def test_order_avg_price(self):
        resp = shop(self.factory.get("/search/shop?name=&order=avg_price&page=1&limit=20"))
        self.assertEqual([int(obj['name']) for obj in json.loads(resp.content)['data']], [0, 1, 2, 3])

    def test_order_sales(self):
        resp = shop(self.factory.get("/search/shop?name=&order=sales&page=1&limit=20"))
        self.assertEqual([int(obj['name']) for obj in json.loads(resp.content)['data']], [3, 2, 1, 0])

    def test_order_dist(self):
        resp = shop(self.factory.get("/search/shop?name=&order=dist&loc_lng=114.30433&loc_lat=30.59405&page=1&limit=20"))
        self.assertEqual([int(obj['name']) for obj in json.loads(resp.content)['data']], [3, 0, 2, 1])
