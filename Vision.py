import os
import json, requests


def Vision(img):
    my_secret = os.environ['key']
    url = "https://vision.googleapis.com/v1/images:annotate" + "?key=" + my_secret
    data = {
        "requests": [{
            "features": [{
                "type": "SAFE_SEARCH_DETECTION"
            }],
            "image": {
                "content": img
            }
        }]
    }

    js = requests.post(url=url, data=json.dumps(data))
    dic = json.loads(js.text)

    if 'error' in dic['responses'][0]:
        return 1

    return dic['responses'][0]["safeSearchAnnotation"]
