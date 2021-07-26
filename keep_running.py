import requests, time, base64, os
from Vision import Vision
from bs4 import BeautifulSoup

def ImageProcess(img, conclusion):
    image = str(base64.b64encode(img).decode('UTF-8'))
    result = Vision(image)

    while result == 1:
        time.sleep(1)
        result = Vision(image)

    if (result['adult'] == 'LIKELY') or (result['adult'] == 'VERY_LIKELY') or (result['violence'] == 'LIKELY') or (result['violence'] == 'VERY_LIKELY') or (result['racy'] == 'LIKELY') or (result['racy'] == 'VERY_LIKELY'):
        text = "Sensitive Content Detected\n" + "Adult: " + result['adult'] + "\n" + "Violence: " + result['violence'] + "\n" + "Racy: " + result['racy'] + "\n" + "Medical: " + result['medical'] + "\n" + "Spoof: " + result['spoof']
        print(text)
        return 1
    else:
        print("Clear\n")
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

url = ""
#정식갤러리와 마이너 갤러리의 차이
gallery = input("갤러리 id를 입력하세요: ")
a = input("정식 갤러리면 1, 마이너 갤러리면 0을 입력하세요: ")

if a == '1':
    url = "https://gall.dcinside.com/board/lists"
elif a == '0':
    url = "https://gall.dcinside.com/mgallery/board/lists"

print("\n")

headers = [
    {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67'
    },
]

BASE_URL = "https://gall.dcinside.com"
last_post = ""

while True:
    params = {
        "id": gallery,
        "page": 1
    }
    
    html = requests.get(url, params=params, headers=headers[0]).text

    soup = BeautifulSoup(html, "html.parser")
    try:
        post_list = soup.find('tbody').find_all('tr', class_="ub-content")
    except:
        print("Deleted")
        time.sleep(10)
        continue
    
    for l in post_list:
        if not (l.find('em')['class'][1] == "icon_pic"):
            continue
        
        name = l.find("td", class_="gall_writer")
        if len(name.find("span")['class']) == 2:
            continue
        
        tail = l.find('a', href=True)['href']
        if last_post == tail:
            break
        else:
            url = BASE_URL + tail
            try:
                search(url)
            except:
                print("Deleted")
            last_post = tail
            break		

    time.sleep(5)