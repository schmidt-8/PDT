import requests
import json


js_file = open('dump.jsonl', encoding='utf8')

payload = ""

for line in js_file:
    payload += '{ "index": { "_index": "tweets" } }\n' + line

res = requests.post('http://localhost:9200/tweets/_bulk', 
headers={'Content-Type': 'application/x-ndjson'},
data=payload.encode('utf8'))

print(res.text)