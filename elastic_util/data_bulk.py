import requests, json, os
from datetime import datetime
from elasticsearch import Elasticsearch
from tqdm import tqdm

INDEX_NAME = 'revd'

directory_path = 'path'
res = requests.get('http://localhost:9200')
es = Elasticsearch([{'host':'localhost','port':'9200'}])

es.indices.create(
    index=INDEX_NAME,
    body={
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
        "mappings": {
            "dynamic": "true",
            "_source": {
            "enabled": "true"
            },
            "properties": {
                "id": {
                    "type": "long"
                },
                "res_id": {
                    "type": "text"
                },
                "res_name": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
                "adress": {
                    "type": "text",
                    "fields": {
                        "nori": {
                            "type": "text",
                            "analyzer": "my_analyzer"
                        }
                    }
                },
                "comment": {
                    "type": "text",
                    "fields": {
                        "nori": {
                            "type": "text",
                            "analyzer": "my_analyzer"
                        }
                    }
                },
                "keywords": {
                    "type": "keyword",
                    "fields": {
                        "nori": {
                            "type": "text",
                            "analyzer": "my_analyzer"
                        }
                    }
                },
                "comment_vector": {
                    "type": "dense_vector",
                    "dims": 768
                }
            }
        }
    }
)

# 여러 개의 데이터를 한 번에 Elasticsearch에 삽입하는 방법인 bulk를 사용하여 백과사전 데이터를 Elasticsearch에 삽입
directory_path = '/home/ubuntu/hot6/data/posts/posts_2021-03-30_08-38-34.json'
with open(directory_path, encoding='utf-8') as json_file:
    json_data = json.loads(json_file.read())

body = ""
count = 1
for i in tqdm(json_data):
    if (count % 1000) == 0:
        es.bulk(body)
        body = ""
    body = body + json.dumps({"index": {"_index": INDEX_NAME, "_id": count}}) + '\n'
    body = body + json.dumps(i, ensure_ascii=False) + '\n'
    if count == 1:
        print(body)
    count += 1

# output_file_path = '/home/ubuntu/hot6/data/posts/indices_'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+'.json'
# f = open(output_file_path, 'w')
# f.write(body)
# f.close()

es.bulk(body)