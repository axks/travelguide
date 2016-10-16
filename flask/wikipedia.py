import requests
import json

endpoint = "https://en.wikipedia.org/w/api.php"
queryImages = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=%s&prop=images"
queryInfo = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=%s"

googleImages = "https://www.googleapis.com/customsearch/v1?q=%s&num=1"


respInfo = requests.get(queryInfo %("bremen"))
d = json.loads(respInfo.text)


print(d)
