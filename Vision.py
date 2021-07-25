from google.cloud import vision


def Vision(img):
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
	
	if response.error.message:
		return 1
	
	return result
