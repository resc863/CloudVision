import json, os
from google.cloud import vision

#Google Cloud SDK의 사용 인증을 
#GOOGLE_APPLICATION_CREDENTIALS 환경 변수에 넣습니다

def Vision(img):
	data = os.environ['auth']
	file_data = json.loads(data)
	
	with open('/home/runner/CloudVision/auth.json', 'w', encoding="utf-8") as make_file:
		json.dump(file_data, make_file, ensure_ascii=False, indent="\t")

	client = vision.ImageAnnotatorClient()
	image = vision.Image(content=img)

	response = client.safe_search_detection(image=image)
	safe = response.safe_search_annotation
	
	likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
	
	result = {}
	result['adult'] = likelihood_name[safe.adult]
	result['violence'] = likelihood_name[safe.violence]
	result['spoof'] = likelihood_name[safe.spoof]
	result['medical'] = likelihood_name[safe.medical]
	result['racy'] = likelihood_name[safe.racy]

	file = '/home/runner/CloudVision/auth.json'

	if os.path.isfile(file):
		os.remove(file)
	
	if response.error.message:
		return 1
	
	return result
