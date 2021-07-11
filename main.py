from bs4 import BeautifulSoup
import requests, time, base64
from Vision import Vision

url = "https://gall.dcinside.com/mgallery/board/lists?id=elsa"
headers = [
	{
		'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67'
	},
]

BASE_URL = "https://gall.dcinside.com"
url_list = []

for i in range(1, 4):
	params = {
		"id" : "elsa",
		"pages" : i
	}

	html = requests.get(url, params=params, headers=headers[0]).text
	soup = BeautifulSoup(html, "html.parser")
	post_list = soup.find('tbody').find_all('tr')

	for l in post_list:
		#print(l['data-type'])
		if not (l['data-type'] == "icon_pic"):
			continue
		tail = l.find('a', href=True)['href']
		final_url = BASE_URL + tail
		#print(final_url)
		url_list.append(final_url)

for i in url_list:
	conclusion = False

	html = requests.get(i, headers=headers[0]).text
	soup = BeautifulSoup(html, "html.parser")
	div = soup.find("ul", class_="appending_file")
	lis = div.find_all("li")

	title = soup.find("span", class_="title_subject").string
	print(title)
	
	for li in lis:
		img = li.find("a")['href']
		
		if conclusion is True:
			continue
		else:
			file_ext = img.split('.')[-1]
        	#저장될 파일명
			savename = img.split("no=")[2]
			headers[0]['Referer'] = i
			response = requests.get(img, headers=headers[0])

        	#path = f"Image/{savename}"
            #file = open(path, "wb") #경로 끝에 [1] 을 추가해 받는다.
            #file.write(response.content)
        	#file.close()

			result = Vision(str(base64.b64encode(response.content).decode('UTF-8')))
			print(result)










