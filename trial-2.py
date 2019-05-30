# taken from : https://docs.microsoft.com/en-us/azure/cognitive-services/bing-image-search/quickstarts/python
import functions as f

import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
# import urllib.request
import urllib
import json

subscription_key = "a80556b34a9b42c386f65d3618b896be"
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
search_term = "cars"

headers = {"Ocp-Apim-Subscription-Key" : subscription_key}

# api reference: https://dev.cognitive.microsoft.com/docs/services/8336afba49a84475ba401758c0dbf749/operations/56b4433fcf5ff8098cef380c
params  = {"q": search_term, "license": "public", "imageType": "photo", "offset" : "0", "count" : "500"}

response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()
num_results = len(search_results['value'])

data = { "images" : [] }

for i in range(0,num_results):
    print(search_results['value'][i]['contentUrl'])

    result = search_results['value'][i]
    entry = {}

    entry['content_url'] = result['contentUrl']
    entry['name'] = result['name']
    entry['search_term'] = search_term
    entry['encode_format'] = result['encodingFormat']
    entry['width'] = result['width']
    entry['height'] = result['height']
    entry['creative_commons'] = result['creativeCommons']
    entry['id'] = "none"
    entry['validation'] = "none"
    entry['fname'] = "none"

    data["images"].append(entry)

    # try:
    #     f.save_image(content_url, encoding_format, directory="./storage/", file_name=str(i))
    # except:
    #     print("DOESNT WORK!")

next_offset = search_results['nextOffset']
print("Number of results {}".format(num_results))

# write to JSON here
with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)

print("Finished?")
