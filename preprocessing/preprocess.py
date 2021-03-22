import csv
from funcs import remove_space, remove_comma
import pandas as pd

## 메뉴판 닷컴 전처리
def menupan_preprocessing(file_name):
    # file = 'menupan.csv'
    f = open('./' + file_name, 'r', encoding='utf-8-sig')
    f2 = open('menupan2.csv', 'w')
    contents = csv.reader(f)                            # 파일 읽기
    count = 0

    f2.write('식당이름' + ',' + '음식분류' + ',' + '주소' + ',' + 'URL' + ',' + '총평점' + ',' 
    + '식당특징' + ',' + '영업시간' + ',' + '좌석개수' + ',' + '흡연여부' + ',' + '인터넷유무' + ',' 
    + '주차유무' + ',' + '식당설명' + ',' + '리뷰' + ',' + '작성날짜' + ',' + '개별평점' + '\n')
    for line in contents:               # 파일 한 줄(행, row)씩 읽기
        count += 1
        if count == 1:
            continue
        date_data = line[13].split('\n')
        score_data = line[14].split('\n')
        reviews = line[12].split('@@\n')
        for i in range(12):
            line[i] = remove_comma(line[i])

        for i in range(len(date_data)):
            reviews[i] = remove_comma(reviews[i])
            f2.write(line[0] + ',' + line[1] + ',' + line[2] + ',' + line[3] + ',' + line[4] + ',' 
            + line[5] + ',' + line[6] + ',' + line[7] + ',' + line[8] + ',' + line[9] + ',' 
            + line[10] + ',' + line[11] + ',' + reviews[i] + ',' + date_data[i] + ',' + score_data[i] + '\n')

    f2.close()
    f.close()


# 메뉴판닷컴 데이터 추출(식당이름, 주소, 리뷰추출, 데이터들을 dataframe 형태로 반환)
def menupan_data_extraction(file_name):
    df = pd.read_csv('./' + file_name)
    drop_columns = []
    remain_columns = ['식당이름', '주소', '리뷰']
    for c in df.columns:
        if c not in remain_columns:
            drop_columns.append(c)

    df.drop(drop_columns, axis='columns', inplace=True)
    return df


# 다이닝코드 데이터 추출(식당이름, 주소, 리뷰추출, 데이터들을 dataframe 형태로 반환)
def diningcode_date_extraction(file_name):
    # file = './review_final.csv'
    df = pd.read_csv('./' + file_name)
    drop_columns = []
    remain_columns = ['식당이름', '주소', '리뷰']
    for c in df.columns:
        if c not in remain_columns:
            drop_columns.append(c)
    
    df.drop(drop_columns, axis='columns', inplace=True)
    return df


# 트립어드바이저 데이터 추출(식당이름, 주소, 리뷰추출, 데이터들을 dataframe 형태로 반환)
def tripadvisor_date_extraction(file_name):
    # file = './review_final.csv'
    df = pd.read_csv('./' + file_name)
    drop_columns = []
    remain_columns = ['식당이름', '주소', '리뷰']   # 이 부분 수정 필요
    for c in df.columns:
        if c not in remain_columns:
            drop_columns.append(c)
    
    df.drop(drop_columns, axis='columns', inplace=True)
    #df = df[['Restaurant', 'Address', 'Review']]    # 컬럼 순서 정렬
    #df = df.rename(columns={'Restaurant':'식당이름', 'Address':'주소', 'Review':'리뷰'})  # 컬럼 이름 변경
    return df


# 망고플레이트 데이터 추출(식당이름, 주소, 리뷰추출, 데이터들을 dataframe 형태로 반환)
def mangoplate_data_extraction(file_name):
    df = pd.read_csv('./' + file_name)
    df = df.rename(columns={'RES_NAME':'식당이름', 'RES_ADDRESS':'주소', 'REV_COMMENT':'리뷰'})  # 컬럼 이름 변경
    drop_columns = []
    remain_columns = ['식당이름', '주소', '리뷰']
    for c in df.columns:
        if c not in remain_columns:
            drop_columns.append(c)
    
    df.drop(drop_columns, axis='columns', inplace=True)
    df = df[['식당이름', '주소', '리뷰']]    # 컬럼 순서 정렬
    return df


# 요기요 데이터 추출(식당이름, 주소, 리뷰추출, 데이터들을 dataframe 형태로 반환)
def yogiyo_data_extraction(file_name):
    df = pd.read_csv('./' + file_name)
    drop_columns = []
    remain_columns = ['Restaurant', 'Address', 'Review']
    for c in df.columns:
        if c not in remain_columns:
            drop_columns.append(c)
    
    df.drop(drop_columns, axis='columns', inplace=True)
    df = df[['Restaurant', 'Address', 'Review']]    # 컬럼 순서 정렬
    df = df.rename(columns={'Restaurant':'식당이름', 'Address':'주소', 'Review':'리뷰'})  # 컬럼 이름 변경
    return df


# 데이터 추출의 메인함수
def data_extraction(file_list, main_file):
    result = pd.read_csv('./' + main_file)
    df = pd.DateFrame()     # file_list = [[name, type], []]
    for f, site_type in file_list:
        if site_type == 'yogiyo':
            df = yogiyo_data_extraction(f)
        elif site_type == 'mangoplate':
            df = mangoplate_data_extraction(f)
        elif site_type == 'tripadvisor':
            df = tripadvisor_date_extraction(f)
        elif site_type == 'diningcode':
            df = diningcode_date_extraction(f)
        elif site_type == 'menupan':
            df = menupan_data_extraction(f)
        result = pd.concat([result, df])
    
    result.to_csv('total_review.csv')
    merge_same_restaurant('total_review.csv')


# 같은 식당끼리의 리뷰 데이터 통합
def merge_same_restaurant(file_name):
    df = pd.read_csv('./' + file_name)
    restaurants = df['식당이름'].unique()
    new_df = pd.DataFrame()
    for j, r in enumerate(restaurants):
        restaurant = df[df[r] == r]   # 식당이름이 같은 식당들의 데이터에 접근
        reviews = []
        address = restaurant.iloc[0, 2]
        for i in range(len(restaurant)):
            review = restaurant.iloc[i, 3]
            reviews.append(review)
        new_df.loc[j] = [r, address, reviews]

    new_df.to_csv('merge_review.csv')





df = pd.read_csv('./data/review_final2.csv')
restaurants = df['식당이름'].unique()
new_df = pd.DataFrame(columns=['식당이름','주소','리뷰'])
for j, r in enumerate(restaurants):
    restaurant = df[df['식당이름'] == r]   # 식당이름이 같은 식당들의 데이터에 접근
    reviews = []
    address = restaurant.iloc[0, 2]
    for i in range(len(restaurant)):
        review = restaurant.iloc[i, 3]
        reviews.append(review)
    new_df.loc[j] = {'식당이름': r, '주소': address, '리뷰': reviews}

new_df.to_csv('merge_review.csv')
