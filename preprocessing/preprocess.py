import csv
from funcs import remove_space, remove_comma

## 메뉴판 닷컴 전처리

f = open('menupan.csv', 'r', encoding='utf-8-sig')
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