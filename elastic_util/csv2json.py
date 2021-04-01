#-*- coding:utf-8 -*-
from datetime import datetime

import csv, json
import ast # for '[,]' -> [,]
from tqdm import tqdm

from sentence_transformers import SentenceTransformer, util


input_file_path = '/home/ubuntu/hot6/data/hot6_db_keysentences_2021-03-26_05-13-18.csv'
output_file_path = '/home/ubuntu/hot6/data/posts/posts_'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+'.json'
model_path = '/home/ubuntu/hot6/bh/KoSentenceBERT_SKTBERT/output/training_stsbenchmark_skt_kobert_model_-2021-03-28_05-25-43_best'
embedder = SentenceTransformer(model_path)

def check_comment(s):
    if s.isspace() == True:
        return True
    if len(s) > 500:
        return True
    return False

with open(input_file_path, "r", encoding="utf-8-sig", newline="") as input_file, \
        open(output_file_path, "w", encoding="utf-8", newline="") as output_file:

    fieldnames = ("id", "res_id", "res_name", "adress", "comment", "keywords")
    reader = csv.DictReader(input_file, fieldnames)
    next(reader, None)  # skip the headers
    docs = [] # JSON 객체를 담습니다. 
    for row in tqdm(reader, desc="csv2json...", mininterval=0.01):
        if check_comment(row["comment"]):
            continue
        vectors = embedder.encode(row["comment"], convert_to_tensor=True)
        query_vector = [vector.tolist() for vector in vectors]
        row.update({'comment_vector':query_vector})
        row["keywords"] = ast.literal_eval(row["keywords"])
        docs.append(row)
    print(json.dumps(docs, ensure_ascii=False), file=output_file)
    