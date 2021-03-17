from konlpy.tag import Kkma
from konlpy.utils import pprint
import csv
from preprocessing import preprocessing

def tokenization(text):
    pass

kkma = Kkma()
# pprint(kkma.sentences(u'네, 안녕하세요. 반갑습니다.'))
# print(kkma.sentences(u'네, 안녕하세요. 반갑습니다.'))

f = open('review.csv', 'r', encoding='cp949')       # 리뷰가 저장되어 있는 파일 열기, encoding을 cp949로 해야 함(한국어)
contents = csv.reader(f)                            # 파일 읽기
reviews = []
for line in contents:               # 파일 한 줄(행, row)씩 읽기
    # print(line)                   
    reviews.append(line[-1])        # 한 행은 식당이름, 주소, 평점, 특징, 리뷰내용으로 이뤄져있음
                                    # 리뷰내용만을 가져온다.


# 토큰화하기 전에 전처리를 먼저 실행해준다.

print(reviews)
tokenizations = []
for review in reviews:
    text = preprocessing(review)
    tokenizations.append(kkma.sentences(text))
    print(tokenizations[-1])

f.close()
