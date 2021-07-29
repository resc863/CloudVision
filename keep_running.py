import requests, time, base64, os
from Vision import Vision
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def ProcessGIF(img):
    im = Image.open(img)
    count = 0

    # To iterate through the entire gif
    try:
        while 1:
            im.seek(im.tell()+1)
            count = count + 1
    except EOFError:
        pass # end of sequence

    im.seek(0)
    buffered = BytesIO()
    im.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('UTF-8')
    result = Vision(str(img_str))

    if (result['adult'] == 'LIKELY') or (result['adult'] == 'VERY_LIKELY') or (result['violence']== 'LIKELY') or (result['violence'] == 'VERY_LIKELY') or (result['racy'] == 'LIKELY') or (result['racy']== 'VERY_LIKELY'):
        text = "Sensitive Content Detected\n" + "Adult: " + result['adult'] + "\n" + "Violence: " + result['violence'] + "\n" + "Racy: " + result['racy'] + "\n" + "Medical: " + result['medical'] + "\n" + "Spoof: " + result['spoof']
        print(text)
        return 1
    else:
        print("Clear\n")
        pass
    
    im.seek(count)
    buffered = BytesIO()
    im.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('UTF-8')
    result = Vision(str(img_str))
    
    if (result['adult'] == 'LIKELY') or (result['adult'] == 'VERY_LIKELY') or (result['violence']== 'LIKELY') or (result['violence'] == 'VERY_LIKELY') or (result['racy'] == 'LIKELY') or (result['racy']== 'VERY_LIKELY'):
        text = "Sensitive Content Detected\n" + "Adult: " + result['adult'] + "\n" + "Violence: " + result['violence'] + "\n" + "Racy: " + result['racy'] + "\n" + "Medical: " + result['medical'] + "\n" + "Spoof: " + result['spoof']
        print(text)
        return 1
    else:
        print("Clear\n")
        return 0

def ImageProcess(img, conclusion):
    image = str(base64.b64encode(img).decode('UTF-8'))
    result = Vision(image)

    while result == 1:
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

            if img[-3:] == "gif":
                result = ProcessGIF(BytesIO(response.content))
            else:
                result = ImageProcess(response.content)

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
    
    html = requests.get(url, params=params, headers=headers[0])

    if html.status_code != 200:
        print(html.status_code)
        continue

    soup = BeautifulSoup(html.text, "html.parser")
    tbody = soup.find('tbody')
    if tbody is None:
        print("Error 0")
        time.sleep(5)
        continue
    post_list = tbody.find_all('tr', class_="ub-content")
    
    for l in post_list:
        if (not (l.find('em')['class'][1] == "icon_pic")) or (l is None):
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
                print("Error 1")
            last_post = tail
            break		

    time.sleep(5)