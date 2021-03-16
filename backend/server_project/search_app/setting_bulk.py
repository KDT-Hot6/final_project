import requests, json, os
from elasticsearch import Elasticsearch

directory_path = 'path'
res = requests.get('http://localhost:9200')
es = Elasticsearch([{'host':'localhost','port':'9200'}])

es.indices.create(
    index='dictionary',
    body={
        # 한글 형태소 분석기 nori를 통해 데이터를 토크나이징할 수 있도록 설정
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "my_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer"
                        }
                    }
                }
            }
        },
        # Elasticsearch의 인덱스에 들어가는 데이터의 타입을 정의 
        # 설정해준 분석기 ‘my_analyzer’로 title과 content를 분석할 수 있도록 설정
        "mappings": {
            "properties": {
                "Restaurant": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
                "Review": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
                "id": {
                    "type": "long"
                }
            }
        }
    }
)

# 여러 개의 데이터를 한 번에 Elasticsearch에 삽입하는 방법인 bulk를 사용하여 백과사전 데이터를 Elasticsearch에 삽입
directory_path = '/Users/byeongheon/programmers/final_project/data/'
with open(directory_path + 'test.json', encoding='utf-8') as json_file:
    json_data = json.loads(json_file.read())

body = ""
count = 1
for i in json_data:
    body = body + json.dumps({"index": {"_index": "dictionary", "_id": count}}) + '\n'
    body = body + json.dumps(i, ensure_ascii=False) + '\n'
    if count == 1:
        print(body)
    count += 1

f = open(directory_path+'input.json', 'w')
f.write(body)
f.close()

es.bulk(body)