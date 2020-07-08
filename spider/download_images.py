import json

import requests

if __name__ == '__main__':
    with open('images.json', 'r') as f:
        images = json.load(f)
    finished = 0
    for img, url in images:
        if url != '':
            if url.startswith('//'):
                url = 'http:' + url
            resp = requests.get(url).content
            with open('../view/static/images/' + img, 'wb') as f:
                f.write(resp)
        finished += 1
        print('Downloading image {0}/{1}'.format(finished, len(images)))
