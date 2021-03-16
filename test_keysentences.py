import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt

import krwordrank
from krwordrank.word import KRWordRank
from krwordrank.sentence import make_vocab_score
from krwordrank.sentence import MaxScoreTokenizer
from krwordrank.sentence import keysentence
from krwordrank.sentence import summarize_with_sentences

# 사용하실 때, data 변수에 사용하고자 하는 csv 파일을 첨부해서 사용해주시면 감사하겠습니다. 

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

def get_(item_list):
    pass

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
        min_count = 2, # 단어의 최소 출현 빈도수 (그래프 생성 시)
        max_length = 10, # 단어의 최대 길이
        verbose = True
    )
    keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter, num_keywords=100)
    return keywords, rank, graph

# 데이터 로드 
data = pd.read_csv('/Users/byeongheon/programmers/data/(연대 근처) 37.560873_126.9353833_df.csv')
print(data.columns)

train_data = data[['Restaurant','Menu', 'Review', 'Total', 'OperationTime', 'Address']]
print("train 데이터 - 초기 갯수: "+ str(len(train_data)))
train_data = train_data.dropna(how = 'any') # Null 값이 존재하는 행 제거
print(train_data.isnull().values.any()) # Null 값이 존재하는지 확인
print("train 데이터 - null을 제외한 갯수: "+ str(len(train_data)))

# 리뷰 관련 전처리
# 정규 표현식을 통한 한글 외 문자 제거
train_data['Review'] = train_data['Review'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

# 별점 관련 전처리
# 별점이 4 이상이면 긍정, 3 이하면 부정 
devide_rates(train_data)

# 레스토랑 리스트 추출
restaurants = get_unique_items(train_data)

count = 0
# 레스토랑 리스트를 하나씩 확인하면서 해당하는 긍부정 모델 학습
for restaurant in restaurants:
    res_data = train_data[train_data['Restaurant'] == restaurant]
    pos, neg = get_pos_neg_texts(res_data)

    if count == 56:
        print(len(pos))
        print(len(neg))
        stopwords = {'진짜','정말','너무','맛있게','맛있','잘먹었습니다','먹었습니다','ㅎㅎ','그리고','자주','오랜만에','좋았습니다','번창하세요','배달','빠르고','감사합니다','주문'}
       
        if len(pos) > 5:
            pos_keywords, pos_rank, pos_graph = get_wordrank_keywords(pos)
            print(pos_keywords)
            vocab_score = make_vocab_score(pos_keywords, stopwords, scaling=lambda x:1)
            tokenizer = MaxScoreTokenizer(vocab_score)
            penalty = lambda x: 0 if 25 <= len(x) <= 80 else 1

            sents = keysentence(
                vocab_score, pos, tokenizer.tokenize,
                penalty=penalty,
                diversity=0.3,
                topk=10
            )

            for sent in sents:
                print(sent)


       # neg_keywords, neg_rank, neg_graph = get_wordrank_keywords(neg)
        # print(neg_keywords)
        
        

    count += 1