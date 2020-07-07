import json
import math
import re

import requests

# Algorithm to decode China coordinates to real longitude and latitude.
# Provided by https: // blog.csdn.net / goodnew / article / details / 82622817. 

x_PI = 3.14159265358979324 * 3000.0 / 180.0

PI = 3.1415926535897932384626
a = 6378245.0
ee = 0.00669342162296594323


def wgs84togcj02(lng, lat):
    lat = +lat
    lng = +lng
    if out_of_china(lng, lat):
        return lng, lat
    else:
        d_lat = transform_lat(lng - 105.0, lat - 35.0)
        d_lng = transform_lng(lng - 105.0, lat - 35.0)
        rad_lat = lat / 180.0 * PI
        magic = math.sin(rad_lat)
        magic = 1 - ee * magic * magic
        sqrt_magic = math.sqrt(magic)
        d_lat = (d_lat * 180.0) / ((a * (1 - ee)) / (magic * sqrt_magic) * PI)
        d_lng = (d_lng * 180.0) / (a / sqrt_magic * math.cos(rad_lat) * PI)
        return lng + d_lng, lat + d_lat


def gcj02towgs84(lng, lat):
    lat = +lat
    lng = +lng
    if out_of_china(lng, lat):
        return lng, lat
    else:
        mglng, mglat = wgs84togcj02(lng, lat)
        return lng * 2 - mglng, lat * 2 - mglat


def transform_lat(lng, lat):
    lat = +lat
    lng = +lng
    ret = transform(lng)
    ret += -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
    return ret


def transform_lng(lng, lat):
    lat = +lat
    lng = +lng
    ret = transform(lng)
    ret += 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
    return ret


def transform(lng):
    ret = 0
    ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * PI) + 40.0 * math.sin(lng / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * PI) + 300.0 * math.sin(lng / 30.0 * PI)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    lat = +lat
    lng = +lng
    return not (73.66 < lng < 135.05 and 3.86 < lat < 53.55)


# In case something goes wrong, just copy your browser cookie (http://meishi.meituan.com/i/) here
uuid = 'e9fc82a6d5a945a3ac63.1593604946.1.0.0'
cookies = '__mta=44422811.1594103361171.1594108028584.1594109250051.8; __mta=44422811.1594103361171.1594109223679.1594109230304.7; uuid=e9fc82a6d5a945a3ac63.1593604946.1.0.0; ci=45; rvct=30%2C45; _lxsdk_cuid=17327d94271c8-03f706d62c112e-30634644-1fa400-17327d9427296; lat=29.557459; lng=106.573502; _hc.v=afcfd436-54a6-e9f6-5e17-9ec68925761d.1594101427; _lxsdk=0D421CE859B3C2E34C8633F75EB164BD5C5F7E12F7285584E5EE8F2AF40EEDBC; IJSESSIONID=1txahf2q4kh6g18y4bcckmyaon; iuuid=0D421CE859B3C2E34C8633F75EB164BD5C5F7E12F7285584E5EE8F2AF40EEDBC; cityname=%E9%87%8D%E5%BA%86; webp=1; i_extend=C_b1Gimthomepagecategory11H__a; latlng=29.519489,106.513955,1594103351759; __utma=74597006.422400348.1594103342.1594103342.1594103342.1; __utmc=74597006; __utmz=74597006.1594103342.1.1.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/xing851483876/article/details/81842329; ci3=1; client-id=9b9b1af7-e75b-44e4-bb58-c4e049c7ea25; meishi_ci=45; cityid=45; logan_session_token=gd1xzexihqjzbvethbqn; logan_custom_report=; _lx_utm=utm_source%3Dblog.csdn.net%26utm_medium%3Dreferral%26utm_content%3D%252Fxing851483876%252Farticle%252Fdetails%252F81842329'


def get_common_params(is_json=True):
    payload = {
        'uuid': uuid,
        'version': '8.2.0',
        'platform': 3,
        'app': '',
        'partner': 126,
        'riskLevel': 1,
        'optimusCode': 10,
        'originUrl': 'http://meishi.meituan.com'
    }
    headers = {
        'Host': 'meishi.meituan.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Referer': 'https://meishi.meituan.com/',
        'Cookie': cookies,
    }
    if is_json:
        headers.update({'Content-Type': 'application/json'})
    return payload, headers


def fetch_shop(page, limit):
    payload, headers = get_common_params()
    payload.update({
        'offset': (page - 1) * limit,
        'limit': limit,
        'cateId': 0,
        'lineId': 0,
        'stationId': 0,
        'areaId': 0,
        'sort': 'default',
        'deal_attr_23': '',
        'deal_attr_24': '',
        'deal_attr_25': '',
        'poi_attr_20043': '',
        'poi_attr_20033': ''
    })
    url = 'https://meishi.meituan.com/i/api/channel/deal/list'
    resp = json.loads(requests.post(url, data=json.dumps(payload), headers=headers).content)['data']['poiList'][
        'poiInfos']
    data = []
    for shop in resp:
        lng, lat = gcj02towgs84(shop['lng'], shop['lat'])
        poi_id, poi_ct = shop['poiid'], shop['ctPoi']
        _, html_headers = get_common_params(False)
        html = requests.get(f'http://meishi.meituan.com/i/poi/{poi_id}?ct_poi={poi_ct}',
                            headers=html_headers).content.decode()
        obj = {
            'name': shop['name'],
            'image': shop['frontImg'],
            'addr': re.search('\\"addr\\":\\"([^\\"]+)\\"', html).group(1),
            'loc_lng': lng,
            'loc_lat': lat,
            'avg_price': 100 * shop['avgPrice'],
            'phone': re.search('\\"phone\\":\\"([^\\"]+)\\"', html).group(1),
            'dishes': fetch_dish(poi_id)
        }
        data.append(obj)
        print('Fetched shop {0}/{1}'.format(len(data), len(resp)))
    return data


def fetch_dish(poi_id):
    payload, headers = get_common_params()
    payload.update({
        'poiId': poi_id
    })
    url = 'http://meishi.meituan.com/i/api/dish/poi'
    resp = json.loads(requests.post(url, data=json.dumps(payload), headers=headers).content)['data']['list']
    data = []
    for dish in resp:
        obj = {
            'name': dish['name'],
            'image': dish['frontImgUrl'],
            'price': dish['price']
        }
        data.append(obj)
    return data


if __name__ == '__main__':
    with open('spider.json', 'w') as f:
        json.dump(fetch_shop(1, 100), f)
