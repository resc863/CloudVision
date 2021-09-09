import requests, time, base64
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

def ImageProcess(img):
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
        "Connection" : "keep-alive",
        "Cache-Control" : "max-age=0",
        "sec-ch-ua-mobile" : "?0",
        "DNT" : "1",
        "Upgrade-Insecure-Requests" : "1",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site" : "none",
        "Sec-Fetch-Mode" : "navigate",
        "Sec-Fetch-User" : "?1",
        "Sec-Fetch-Dest" : "document",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language" : "ko-KR,ko;q=0.9"
    },
    {
        "Connection" : "keep-alive",
        "Cache-Control" : "max-age=0",
        "DNT" : "1",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55"
    }
]

BASE_URL = "https://gall.dcinside.com"
read_post = []
i = 0

while True:
    params = {
        "id": gallery,
        "page": 1
    }
    
    html = requests.get(url, params=params, headers=headers[0])
    
    if html.status_code != 200:
        time.sleep(5)
        continue

    soup = BeautifulSoup(html.text, "html.parser")
    tbody = soup.find('tbody')
    if tbody is None:
        print("Error 0")
        time.sleep(5)
        continue

    b = []
    post_list = tbody.find_all('tr', class_="ub-content")

    for k in range(len(post_list)):
        b.append(post_list[len(post_list)-k-1])
    
    for l in b:
        flag = False
        if (not (l.find('em')['class'][1] == "icon_pic")) or (l is None):
            continue
        
        name = l.find("td", class_="gall_writer")
        if len(name.find("span")['class']) == 2:
            continue
        
        tail = l.find('a', href=True)['href']

        for j in read_post:
            if tail == j:
                flag = True
        
        if flag is True:
            continue

        if len(read_post) > 50:
            del read_post[0:]

        url1 = BASE_URL + tail
        try:
            search(url1)
        except:
            print("Error 1")

        read_post.append(tail)		

    time.sleep(5)