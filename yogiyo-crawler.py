import re
import time
import pickle
import pandas as pd
from tqdm import tqdm
from tqdm import trange
import warnings
warnings.filterwarnings('ignore')

import requests
from urllib.request import urlopen, Request
from fake_useragent import UserAgent
import json

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

#스크롤 내리기 
def scroll_bottom():
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    
# 1. 해당 카테고리 음식점 리스트 리턴
def get_restaurant_list(lat, lng, items = 100):
    restaurant_list=[]
    # 헤더 선언 및 referer, User-Agent 전송
    headers = {
        'referer' : 'https://www.yogiyo.co.kr/mobile/',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
        'Accept': 'application/json',
        'x-apikey': 'iphoneap',
        'x-apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2'
    }
    params = {'items':items, 'lat':lat, 'lng':lng, 'order':'distance', 'page':0 ,'search':''}
    host = 'https://www.yogiyo.co.kr'
    path = '/api/v1/restaurants-geo/'
    url = host+path

    response = requests.get(url,headers=headers,params=params)
    
    count = 0
    for item in response.json()['restaurants']:
        restaurant_list.append(item['id'])
        count += 1
    print(restaurant_list)
    return list(set(restaurant_list))

# 2. 검색한 음식점 페이지 들어가기 
def go_to_restaurant(id):
    try:
        restaurant_url = 'https://www.yogiyo.co.kr/mobile/#/{}/'.format(id)
        driver.get(url=restaurant_url)
        print(driver.current_url)
    except Exception as e:
        print('go_to_restaurant 에러')
    time.sleep(5)

# 3-1. 해당 음식점의 정보 페이지로 넘어가기
def go_to_info():
    print('정보 페이지 로드중...')
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[3]/a').click()
    time.sleep(2)
    print('정보 페이지 로드 완료!')

# 3-2. 정보 더보기 클릭하기
def get_info():
    op_time = driver.find_element_by_xpath('//*[@id="info"]/div[2]/p[1]/span').text
    addr = driver.find_element_by_xpath('//*[@id="info"]/div[2]/p[3]/span').text
    print(op_time)
    print(addr)
    return op_time, addr


# 4-1. 해당 음식점의 리뷰 페이지로 넘어가기
def go_to_review():
    print('리뷰 페이지 로드중...')
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a').click()
    time.sleep(2)
    print('리뷰 페이지 로드 완료!')

# 4-2. 리뷰 더보기 클릭하기 
def click_more_review():
    driver.find_element_by_class_name('btn-more').click()
    time.sleep(2)
    
# 5. 리뷰 페이지 모두 펼치기
def stretch_review_page():
    review_count = int(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a/span').text)
    click_count = int((review_count/10))
    print('모든 리뷰 불러오기 시작...')
    for _ in trange(click_count):
        try:
            scroll_bottom()
            click_more_review()
        except Exception as e:
            pass
    scroll_bottom()
    print('모든 리뷰 불러오기 완료!')
        
# 6. 해당 음식점의 모든 리뷰 객체 리턴
def get_all_review_elements():
    reviews = driver.find_elements_by_css_selector('#review > li.list-group-item.star-point.ng-scope')
    return reviews
        
# 7. 페이지 뒤로 가기 (한 음식점 리뷰를 모두 모았으면 다시 음식점 리스트 페이지로 돌아감)
def go_back_page():
    print('페이지 돌아가기중...')
    driver.execute_script("window.history.go(-1)")
    time.sleep(2)
    print('페이지 돌아가기 완료!'+'\n')
    
# 8. 크롤링과 결과 데이터를 pickle 파일과 csv파일로 저장
def save_pickle_csv(location, yogiyo_df):
    yogiyo_df.to_csv('./data/{}_{}_df.csv'.format(location[0], location[1]))
    pickle.dump(yogiyo_df, open('./data/{}_{}_df.pkl'.format(location[0], location[1]),'wb'))
    print('{} {} pikcle save complete!'.format(location[0], location[1]))

# 9. 크롤링 메인 함수
def yogiyo_crawling(location):
    #데이터 프레임 구조 설정 
    df = pd.DataFrame(columns=['Restaurant','UserID','Menu','Review',
                                   'Total','Taste','Quantity','Delivery','Date','OperationTime','Address'])

    try:
        
        restaurant_list = get_restaurant_list(location[0],location[1],100) # 해당 카테고리 음식점 리스트 받아오기
        
        for restaurant_id in restaurant_list:
            try:
                print('********** ' +str(restaurant_list.index(restaurant_id)+1)
                      +'/'+str(len(restaurant_list))+' 번째 **********')
                
                go_to_restaurant(restaurant_id) # 검색한 음식점 클릭     

                go_to_info() # 음식점 정보창 클릭
                op_time, addr = get_info() # 음식점 영업시간, 주소 받아오기 

                go_to_review() # 해당 음식점의 리뷰페이지로 넘어감
                stretch_review_page() # 해당 음식점의 모든 리뷰를 불러옴

                for review in tqdm(get_all_review_elements()):  # 해당 음식점의 리뷰 수 만큼 데이터를 가져옴
                    try:
                        df.loc[len(df)] = { 
                            'Restaurant':driver.find_element_by_class_name('restaurant-name').text,
                            'UserID':review.find_element_by_css_selector('span.review-id.ng-binding').text,
                            'Menu':review.find_element_by_css_selector('div.order-items.default.ng-binding').text,
                            'Review':review.find_element_by_css_selector('p').text,
                            'Total':str(len(review.find_elements_by_css_selector('div > span.total > span.full.ng-scope'))),
                            'Taste':review.find_element_by_css_selector('div:nth-child(2) > div > span.category > span:nth-child(3)').text,
                            'Quantity':review.find_element_by_css_selector('div:nth-child(2) > div > span.category > span:nth-child(6)').text,
                            'Delivery':review.find_element_by_css_selector('div:nth-child(2) > div > span.category > span:nth-child(9)').text,
                            'Date':review.find_element_by_css_selector('div:nth-child(1) > span.review-time.ng-binding').text,
                            'OperationTime':op_time,
                            'Address':addr
                        }
                    except Exception as e:
                        print('리뷰 페이지 에러')
                        print(e)
                        pass
                    
            except Exception as e:
                print('*** 음식점 ID:'+restaurant_id+' *** 음식점 페이지 에러')
                go_back_page()
                print(e)
                pass
            
            print('음식점 리스트 페이지로 돌아가는중...')
            go_back_page() # 해당 음식점 리뷰를 모두 모았으면 다시 음식점 리스트 페이지로 돌아감
            
    except Exception as e:
        print('음식점 리스트 페이지 에러')
        print(e)
        pass
        
    print('End of [ {} - {} ] Crawling!'.format(location[0], location[1]))
    save_pickle_csv(location, df) # 해당 음식점 리뷰 데이터를 pickle, csv 파일로 저장함
    print('{} {} crawling finish!!!'.format(location[0], location[1]))
    
    return df

# 10. 요기요 크롤링 실행 함수
def start_yogiyo_crawling():

    locations = [[37.560873,126.9353833]]
    
    for location in locations:
        try:
            yogiyo = yogiyo_crawling(location)
        except Exception as e:
            print(e)
            pass

# 크롬 드라이버 경로 설정 (절대경로로 설정하는 것이 좋음)
chromedriver = '/Users/byeongheon/programmers/crawler/chromedriver'
driver = webdriver.Chrome(chromedriver)

url = "https://www.yogiyo.co.kr/mobile/#/"

# fake_useragent 모듈을 통한 User-Agent 정보 생성
useragent = UserAgent()
print(useragent.chrome)
print(useragent.ie)
print(useragent.safari)
print(useragent.random)

# 헤더 선언 및 referer, User-Agent 전송
headers = {
    'referer' : 'https://www.yogiyo.co.kr/mobile/',
    'User-Agent' : useragent.chrome,
    'Accept': 'application/json',
    'x-apikey': 'iphoneap',
    'x-apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2'
}

driver.get(url=url)
print(driver.current_url)

start_yogiyo_crawling()


