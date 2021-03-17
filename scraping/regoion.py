from scraping import extract_review
import csv

stations_f = open('station.csv', 'r', encoding='utf-8-sig')
stations_list = csv.reader(stations_f)
restaurant_dic = {}
review_f = open("review.csv", "w")
review_f.write("식당이름" + ',' + "주소" + ',' + "평점" + ','+ "공감수" + ',' + "특징" + ',' + "리뷰" + "\n")
for station in stations_list:
    print(station[0] +"시작")
    extract_review(station[0], restaurant_dic, review_f)
    print(station[0] +"끝")

stations_f.close()
review_f.close()


# 서울 지하철의 모든 역의 이름이 저장되어 있는 csv파일을 읽어 리스트에 역들을 저장한다.
# for루프를 돌며 모든 역을 검색하도록 한다.
# extract_review 함수에 역을 전달하고, 함수 내에서 chromeDriver를 통해 브라우저에 역을 검색하고, 검색된 식당의 리뷰를 가져온다.
# 이 때, chromeDriver의 경로 설정을 올바르게 해야 한다. (chromeDriver는 컴퓨터에 설치된 크롬 브라우저의 버전에 맞는 것을 다운해야 함)