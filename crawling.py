# from selenium import webdriver
import requests
from requests.models import LocationParseError
from bs4 import BeautifulSoup
import pandas as pd
import re

headers = {'referer': 'https://www.menupan.com/restaurant/onepage_201401/include/',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

# 강남/강북의 각 지역을 숫자로 표시한 리스트
seoul_list = [(255, 218), (350, 201), (53, 202), (51, 203), (10, 217), (55, 204), (76, 205), (43, 206), (63, 207), (185, 209), (71, 210), (231, 211),
              (120, 212), (110, 213), (50, 214), (168, 215), (35, 216), (99, 208), (35, 216), ('a',
                                                                                               'a'), (146, 201), (84, 202), (81, 203), (61, 204), (40, 205), (41, 206), (102, 207), (22, 218),
              (46, 208), (18, 223), (51, 219), (115, 209), (43, 210), (22, 217), (100, 211), (7, 216), (101, 222), (24, 224), (30, 220), (516, 212), (99, 213), (61, 214), (258, 215), (49, 221)]

code = seoul_list[0]
page_num = 0
# 강남 : ss, 강북 : sn
seoul_code = ['ss', 'sn']
sc = 'ss'
# 가로수길 페이지 주소 예시 page : 1,2,3 ...
# https://www.menupan.com/restaurant/bestrest/bestrest.asp?page=1&trec=255&areacode=ss218&pt=wk
# https://www.menupan.com/restaurant/bestrest/bestrest.asp?page=2&trec=255&areacode=ss218&pt=wk
# https://www.menupan.com/restaurant/bestrest/bestrest.asp?page=3&trec=255&areacode=ss218&pt=wk


crawling_data = {'res_name': [], 'res_type': [], 'res_address': [], 'res_homepage': [],
                 'res_score': [], 'res_theme': [], 'res_hour': [], 'res_room': [], 'smoking': [],
                 'amenity': [], 'parking': [], 'res_info': [], 'review': [], 'rev_date': [],
                 'rev_score': []}

# 공백, 줄바꿈 제거 함수


def no_space(text):
    text1 = re.sub(
        '&nbsp; | &nbsp;| \n\n|\t\r|\r\n|\n|\r\n\t\t\t\t\t\t\t\t\t|\t\t\t\t\t\t\t\t\t|자세히보기', '', text)
    text2 = re.sub('\n\n | \r\n', '', text1)

    return text2


for code in seoul_list:
    if type(code[0]) == str:  # (a,a) 일때
        sc = seoul_code[1]

    else:
        # print(code)
        for page_num in range(1, 25):  # 각 지역의 page 넘기기

            data = requests.get(
                f'https://www.menupan.com/restaurant/bestrest/bestrest.asp?page={page_num}&trec={code[0]}&areacode={sc}{code[1]}&pt=wk', headers=headers)
            print(
                f'https://www.menupan.com/restaurant/bestrest/bestrest.asp?page={page_num}&trec={code[0]}&areacode={sc}{code[1]}&pt=wk')
            soup = BeautifulSoup(data.text, 'html.parser')

            # 한 페이지에 보이는 가게들 주소
            restaurant = soup.select(
                'body > div > div.container > div.bestRest > div.ranking > div.rankingList > ul > li')

            # body > div > div.container > div.bestRest > div.ranking > div.rankingList > ul > li:nth-child(1) > p.listName > span.restName > a

            # 음식점 i의 상세 페이지 진입
            for i in restaurant:

                res_name = i.select_one('p.listName > span.restName > a')
                # print(res_name.text)
                # 상세 페이지 url 추출
                detail_page = requests.get(
                    'http://menupan.com' + res_name['href'], headers=headers)
                soup_2 = BeautifulSoup(detail_page.text, 'html.parser')
                ajax_code = res_name['href'][-7:]  # 식당이가진 고유주소 코드 추출
                basic_info = soup_2.select(
                    'body > center > div.WrapMain > div.mainArea01 > div.areaBasic')

                table_info = soup_2.select(
                    'body > center > div.WrapMain > div.mainArea01 > div.tabInfo > div.infoTable')

                # 식당의 기본정보 크롤링
                for detail in basic_info:
                    res_name = detail.select_one(
                        'dl.restName > dd').text
                    crawling_data['res_name'].append(
                        res_name.split('[')[0].strip())
                    res_type = detail.select_one('dl.restType > dd').text
                    crawling_data['res_type'].append(res_type)
                    res_address = detail.select_one('dl.restAdd > dd')
                    if res_address == None:
                        crawling_data['res_address'].append('Nan')
                    else:
                        crawling_data['res_address'].append(res_address.text)

                    res_homepage = detail.select_one(
                        'dl.restHome > dd > a')
                    if res_homepage == None:
                        crawling_data['res_homepage'].append('Nan')
                    else:
                        crawling_data['res_homepage'].append(res_homepage.text)

                    res_score = detail.select_one(
                        'dl.restGrade > dd.rate > p.score > span.total').text
                    crawling_data['res_score'].append(res_score)
                    res_theme = detail.select_one('dl.restTheme > dd')

                    if res_theme == None:
                        crawling_data['res_theme'].append('Nan')
                    else:
                        res_theme = no_space(res_theme.get_text())
                        crawling_data['res_theme'].append(res_theme.strip())

                # 표에있는 식당 상세정보 크롤링
                for detail in table_info:
                    res_hour = detail.select_one(
                        'ul.tableTopA > li:nth-child(1) > dl > dd.txt2')
                    if res_hour == None:
                        crawling_data['res_hour'].append('Nan')
                    else:
                        res_hour = no_space(res_hour.get_text())
                        crawling_data['res_hour'].append(res_hour.strip())

                    res_room = detail.select_one(
                        'ul.tableLR > li:nth-child(1) > dl:nth-child(1) > dd')
                    if res_room == None:
                        crawling_data['res_room'].append('Nan')
                    else:
                        crawling_data['res_room'].append(res_room.text.strip())

                    smoking = detail.select_one(
                        'ul.tableLR > li:nth-child(2) > dl:nth-child(1) > dd')
                    if smoking == None:
                        crawling_data['smoking'].append('Nan')
                    else:
                        crawling_data['smoking'].append(smoking.text.strip())

                    parking = detail.select_one(
                        'li:nth-child(4) > dl:nth-child(1) > dd')
                    if parking == None:
                        crawling_data['parking'].append('Nan')
                    else:
                        crawling_data['parking'].append(parking.text.strip())

                    res_info = detail.select_one(
                        'ul.tableBottom > li > dl > dd > div')
                    if res_info == None:
                        crawling_data['res_info'].append('Nan')
                    else:
                        res_info = no_space(res_info.get_text())
                        crawling_data['res_info'].append(res_info.strip())

                    amenity = detail.select_one(
                        'ul.tableLR > li:nth-child(4) > dl:nth-child(2) > dd')
                    if amenity == None:
                        crawling_data['amenity'].append('Nan')
                    else:
                        crawling_data['amenity'].append(amenity.text)

                # print(crawling_data)

                # review를 뽑아보자!!!!!!!!!!!!!!!!!

                review_url = f'https://www.menupan.com/restaurant/onepage_201401/include/ajax_comment.asp?ac={ajax_code}&pg=1&pz=5&ord=1'

                req = requests.get(
                    review_url)
                review_page = req.content
                soup_3 = BeautifulSoup(review_page, 'lxml')
                last_page = soup_3.select_one('body > div > a.last')
                if last_page != None:
                    last_page = soup_3.select_one('body > div > a.last').text
                else:
                    last_page = 1

                rev_date = ''
                rev_score = ''
                review = ''
                date_check = 0
                for j in range(1, int(last_page)+1):
                    # for j in range(1, 2):
                    review_url_2 = f'https://www.menupan.com/restaurant/onepage_201401/include/ajax_comment.asp?ac={ajax_code}&pg={j}&pz=5&ord=1'
                    req_2 = requests.get(
                        review_url_2)
                    review_page_2 = req_2.content
                    soup_4 = BeautifulSoup(review_page_2, 'lxml')
                    review_infos = soup_4.select(
                        'body > ul > li')
                    # print(len(review_infos))
                    # 리뷰날짜, 스코어, 코멘트 크롤링

                    for i in review_infos:
                        if i.select_one('dl > dd.date') == None:
                            crawling_data['rev_date'].append('Nan')
                            crawling_data['rev_score'].append('Nan')
                            crawling_data['review'].append('Nan')
                            date_check = 1
                            break
                        elif i.select_one('dl > dd.rate > p.score') == None:
                            crawling_data['rev_date'].append('Nan')
                            crawling_data['rev_score'].append('Nan')
                            crawling_data['review'].append('Nan')
                            date_check = 1
                            break

                        elif i.select_one('dl > dd.content') == None:
                            crawling_data['rev_date'].append('Nan')
                            crawling_data['rev_score'].append('Nan')
                            crawling_data['review'].append('Nan')
                            date_check = 1
                            break

                        else:
                            rev_date += i.select_one(
                                'dl > dd.date').text.strip()+'\n'

                            rev_score += i.select_one(
                                'dl > dd.rate > p.score').text.strip()+'\n'

                            review += no_space(i.select_one(
                                'dl > dd.content').text.strip())+'@@' + '\n'
                        # review = no_space(review)
                        # review += review + '\n'
                        # print(res_theme, res_hour)
                if date_check == 1:
                    pass
                else:
                    crawling_data['rev_date'].append(
                        rev_date)
                    crawling_data['rev_score'].append(
                        rev_score)
                    crawling_data['review'].append(review)

                # print(crawling_data)
#             # print(res_name, rev_date, review, rev_score)
crawling = pd.DataFrame.from_dict(crawling_data)

crawling.to_csv('menupan_crawling7.csv')
