# This Python file uses the following encoding: utf-8
import os, sys
from datetime import datetime

import pandas as pd
from tqdm import tqdm

import krwordrank
from krwordrank.word import KRWordRank
from krwordrank.sentence import make_vocab_score
from krwordrank.sentence import MaxScoreTokenizer
from krwordrank.sentence import keysentence
from krwordrank.sentence import summarize_with_sentences

DATA_SAVE_PATH = '/home/ubuntu/hot6/data/hot6_db_keysentences_'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def get_unique_items(df, col = 'RES_NAME'):
    return df[col].unique() 

def get_texts(df, col = 'REV_PRO_COM'):
    texts = []
    if df.empty:
        return [], []
    texts = [review for review in df[col]]
    return texts

# beta : PageRank의 decaying factor beta
def get_wordrank_keywords(texts, beta=0.85, max_iter=10):
    wordrank_extractor = KRWordRank(
        min_count = 3, # 단어의 최소 출현 빈도수 (그래프 생성 시)
        max_length = 10, # 단어의 최대 길이
        verbose = True
    )
    keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter, num_keywords=10)
    return keywords, rank, graph

def save_csv(df):
    df.to_csv(DATA_SAVE_PATH+'.csv')
    print('csv save complete!')

# 데이터 로드 
data = pd.read_csv('/home/ubuntu/hot6/data/hot6_db.csv')
print(data.columns)

train_data = data[['RES_ID_NEW', 'RES_NAME', 'RES_ADDRESS', 'REV_COMMENT', 'REV_PRO_COM']]
print("train 데이터 - 초기 갯수: "+ str(len(train_data)))
train_data = train_data.dropna(how = 'any') # Null 값이 존재하는 행 제거
print(train_data.isnull().values.any()) # Null 값이 존재하는지 확인
print("train 데이터 - null을 제외한 갯수: "+ str(len(train_data)))

# 레스토랑 리스트 추출
restaurants = get_unique_items(train_data, 'RES_ID_NEW')

# stopwords 리스트 
stopwords = {'먹었습니다', '주셔서', '맛있', '너무', '맛이', '정말', '있는', '좋아', '괜찮', '음식', '많이', '진짜', '생각', '느낌', '먹었', '메뉴', '여기', '좋았', '그냥', '먹어', '주문', '먹고', '아니', '먹을', '다른', '조금', '좋은', '들어', '맛은', '정도', '엄청', '있어', '방문', '먹는', '사람', '아주', '하나', '같이', 'ㅎㅎ', '있다', '가게', '별로', '양이', '먹으', '그런', '처음', '같은', '맛도', '그리고', '약간', 'ㅋㅋ', '않고', '있었', '같아요', '좋고', '같아', '살짝', '그래도', '역시', '제일', 'ㅠㅠ', '곳이', '하는', '좋아요', '기대', '나오는', '먹기', '다시', '많아', '식당', '근데', '완전', '하지만', '양도', '시간', '항상', '만족', '시켜', '자주', '시켰는데', '있어서', '같다', '나오', '매우', '자리', '추가', '특히', '맛을', '가장', '식사', '테이블', '사장님', '많고', '많은', '없는', '함께', '나는', '생각보다', '적당', '모두', '친구', '배달', '바로', '좋다', '하고',  '굉장히', '무난', '이런', '저는', '종류', '않은', '요리', '먹었는데', '좋았어요', '아닌', '계속', '기본', '많아서', '그래', '아쉬', '부드', '해서', '편이', '손님', '재료', '근처', '않았', '이렇게', '않아', '한번', '리뷰', '뭔가', '개인적으로', '느껴', '시켰', '직원', '나온', '다음', '있고', '먹으면', '가서', '제가', '비해', '포장', '구워', '잘먹었습니다', '거의', '갔는데', '인분', '빠르고', '그리', '빨리', '내가', '안에', '다만', '공간', '직접', '기분', '그렇', '감사합니다', '먹은', '그런지', '간이', '마시', '기다', '사람이', '적당히', '사실', 'ㅋㅋㅋ', '매장', '동네', '들어가', '위에', '향이', '했는데', '느낌이', '없어', '따로', '일단', '시키', '원래', '없이', '분위', '오늘', '빵이', '친절하', '평범', '면이', '다음에', '대기', '분들', '것이', '맛잇', '가격이', 'ㅜㅜ', '좋네요',  '보니', '위치', '깔끔하고', '오랜만에', '요즘', '가면', '좋을', '때문에', '찾아', '맛있었', '나쁘지', '오래', '들어간', '양은', '맛있어',  '모르겠', '것도',  '맛나', '보통', '냄새' '이곳' '있습니다', '선택', '작은', '가는', '내부', '있음', '그렇게', '모르', '않는', '괜찮은', '사이', '달지', '그래서', '이스크림', '좋아하', '좋습니다', '오픈', '와서', '개인', '집이', '없었', '나왔', '없다', '일반', '좋아하는', '훨씬', '주신', '웨이팅이', '서비', '기억', '밥이', '자체', '넣어', '감사', '여러', '전체적으로', '분위기도', '시킬', '좋았다', '나와', '가득', '구성', '예쁘', '가격도', '우리', '올라', '싶은', '아쉬웠', '이름', '어울', '때문', '하지', '없고', '이상', '상당히', '없어서', '않아서', '조합', '언제나', '합니다',  '아니라', '굳이', '식감이', '한다', '이집', '번창하세요', '단계', '있지만',  '아쉽', '좋았습니다', '모든', '찍어', '가끔', '호점', '워낙', '나름', '있을', '배달도', '부분', '여긴', '중에', '진하고'}

# 레스토랑 리스트를 하나씩 확인하면서 대표 문장 뽑아내기 

res_ks_df = pd.DataFrame(columns=['RES_ID_NEW','RES_NAME','RES_ADDRESS','KEY_COMMENT','KEY_WORDS'])

for restaurant in tqdm(restaurants):
   
    try:
        res_data = train_data[train_data['RES_ID_NEW'] == restaurant]
        res_data.reset_index(drop=True, inplace=True)
        texts = get_texts(res_data)
        
        if len(texts) > 5:
            keywords, rank, graph = get_wordrank_keywords(texts)
            vocab_score = make_vocab_score(keywords, stopwords, scaling=lambda x:1)
            tokenizer = MaxScoreTokenizer(vocab_score)
            penalty = lambda x: 0 if 12 <= len(x) <= 50 else 1

            sents = keysentence(
                vocab_score, texts, tokenizer.tokenize,
                penalty=penalty,
                diversity=0.3,
                topk=5
            )
            
            for sent in sents:
                res_ks_df=res_ks_df.append({
                    'RES_ID_NEW' : res_data.at[0,'RES_ID_NEW'] , 
                    'RES_NAME': res_data.at[0,'RES_NAME'], 
                    'RES_ADDRESS': res_data.at[0,'RES_ADDRESS'],
                    'KEY_COMMENT': sent,
                    'KEY_WORDS': keywords
                    } , ignore_index=True)

    except Exception as e:
        print(e)
        pass

save_csv(res_ks_df)


