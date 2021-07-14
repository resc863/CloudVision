from bs4 import BeautifulSoup
import requests, time, base64
from Vision import Vision


def ImageProcess(img, conclusion):
    image = str(base64.b64encode(img).decode('UTF-8'))
    result = Vision(image)

    while result == 1:
        time.sleep(5)
        result = Vision(image)

    if (result['adult'] == 'LIKELY') or (result['adult'] == 'VERY_LIKELY') or (
            result['violence']
            == 'LIKELY') or (result['violence'] == 'VERY_LIKELY') or (
                result['racy'] == 'LIKELY') or (result['racy']
                                                == 'VERY_LIKELY'):
        text = "Sensitive Content Detected\n" + "Adult: " + result[
            'adult'] + "\n" + "Violence: " + result[
                'violence'] + "\n" + "Racy: " + result['racy']
        print(text)
        return 1
    else:
        print("Clear")
        return 0


def search(url):
    conclusion = False
    html = requests.get(url, headers=headers[0])
    soup = BeautifulSoup(html.text, "html.parser")
    div = soup.find("ul", class_="appending_file")
    lis = div.find_all("li")

    title = soup.find("span", class_="title_subject").string
    print(title)

    for li in lis:
        if conclusion is True:
            break
        else:
            img = li.find("a")['href']
            headers[0]['Referer'] = url
            try:
                response = requests.get(img, headers=headers[0])
            except:
                print('Error')
                print("\n" + url + "\n")
                continue
            result = ImageProcess(response.content, conclusion)
            if result > 0:
                print("\n" + url + "\n")
                conclusion = True


url = "https://gall.dcinside.com/mgallery/board/lists?id=elsa"
headers = [
    {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67'
    },
]

BASE_URL = "https://gall.dcinside.com"
url_list = []

for i in range(1, 3):
    params = {"id": "elsa", "pages": i}

    html = requests.get(url, params=params, headers=headers[0]).text
    soup = BeautifulSoup(html, "html.parser")
    post_list = soup.find('tbody').find_all('tr', class_="ub-content us-post")

    for l in post_list:
        #print(l['data-type'])
        if not (l['data-type'] == "icon_pic"):
            continue
        tail = l.find('a', href=True)['href']
        final_url = BASE_URL + tail
        #print(final_url)
        url_list.append(final_url)

for url in url_list:
    search(url)
