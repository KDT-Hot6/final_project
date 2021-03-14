from collections import defaultdict
import pickle

import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt

import krwordrank
from krwordrank.word import KRWordRank

# 사용하실 때, data 변수에 사용하고자 하는 csv 파일을 첨부해서 사용해주시면 감사하겠습니다. 

def get_hangul_from_df(df, col = 'Review'):
    df[col] = df[col].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
    return df

def get_texts_scores(fname):
    with open(fname, encoding='utf-8') as f:
        docs = [doc.lower().replace('\n','').split('\t') for doc in f]
        docs = [doc for doc in docs if len(doc) == 2]
        
        if not docs:
            return [], []
        
        texts, scores = zip(*docs)
        return list(texts), list(scores)

# negative <= base < positive (neg = 0, pos = 1) 
def devide_rates(df, col = 'Total', base = 3):
    df[col] = df[col].apply(lambda x: 0 if x <= base else 1)
    return df

def get_unique_items(df, col = 'Restaurant'):
    return df[col].unique() 

def get_texts(df, col = 'Review'):
    texts = []
    if df.empty:
        return []
    texts = [review for review in df[col]]
    return texts

def get_pos_neg_texts(df):
    pos, neg = [], []
    if df.empty:
        return [], []
    pos = [review for review, total in zip(df['Review'], df['Total']) if total == 1]
    neg = [review for review, total in zip(df['Review'], df['Total']) if total == 0]

    return pos, neg

# beta : PageRank의 decaying factor beta
def get_wordrank_keywords(texts, beta=0.85, max_iter=10):
    wordrank_extractor = KRWordRank(
        min_count = 4, # 단어의 최소 출현 빈도수 (그래프 생성 시)
        max_length = 10, # 단어의 최대 길이
        verbose = True
    )
    keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter, num_keywords=100)
    return keywords, rank, graph

# 리뷰에서 키워드들을 등장횟수와 함께 추출합니다. cols = [restaurant, review]
def get_keywords_counter(restaurants, train_data, cols):
    counter = defaultdict(lambda: 0)
    for restaurant in restaurants:
        try:
            res_data = train_data[train_data[cols[0]] == restaurant]
            texts = get_texts(res_data, cols[1])
            keywords, rank, graph = get_wordrank_keywords(texts)
            for keyword in keywords.keys():
                counter[keyword] += 1    
        except :
            pass

    res = sorted(counter.items(), key=(lambda x: x[1]), reverse=True)
    return res

# 데이터 로드 
data = pd.read_csv('/Users/byeongheon/programmers/final_project/data/review_final2.csv')
print(data.columns)

#train_data = data[['Restaurant','Menu', 'Review', 'Total', 'OperationTime', 'Address']]
train_data = data[['식당이름','주소', '리뷰']]

print("train 데이터 - 초기 갯수: "+ str(len(train_data)))
train_data = train_data.dropna(how = 'any') # Null 값이 존재하는 행 제거
print(train_data.isnull().values.any()) # Null 값이 존재하는지 확인
print("train 데이터 - null을 제외한 갯수: "+ str(len(train_data)))

# 리뷰 관련 전처리
# 정규 표현식을 통한 한글 외 문자 제거
train_data = get_hangul_from_df(train_data, '리뷰')

# 레스토랑 리스트 추출
restaurants = get_unique_items(train_data, '식당이름')

keywords_counter = get_keywords_counter(restaurants, train_data, ['식당이름', '리뷰'])
with open('keywords_counter.pickle','wb') as fw:
    pickle.dump(keywords_counter, fw)
print(keywords_counter)
