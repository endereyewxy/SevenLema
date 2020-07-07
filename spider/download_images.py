import json

import requests

if __name__ == '__main__':
    with open('images.json', 'r') as f:
        images = json.load(f)
    finished = 0
    for image in images:
        if image != '':
            resp = requests.get(image).content
            with open('../view/static/images/' + image[-36:], 'wb') as f:
                f.write(resp)
        finished += 1
        print('Downloading image {0}/{1}'.format(finished, len(images)))
