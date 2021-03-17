import requests
import urllib
import funcs
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup


def extract_review(station, restaurant_dic, f):
    # "https://www.diningcode.com/list.php?query=%EA%B0%95%EB%8F%99%EC%97%AD"
    # "https://www.diningcode.com/isearch.php?query=강동역"
    # 역을 기반으로 검색
    # 기본 URL은 https://www.diningcode.com/
    # 검색했을 때의 URL은 "https://www.diningcode.com/list.php?query=검색내용" 이다.
    # 따라서, 검색내용(지역이름)만 바꿔주며 각 지역의 식당을 검색한다.
    # 예) 강동역을 검색했을 때
    #     "https://www.diningcode.com/isearch.php?query=강동역"
    #    이 때, 한글이 포함되면 사이트에 접근할 수 없으므로 한글을 URL인코더로 바꿔서 입력해야 한다.
    #    urllib.parse.quote("강동역") -> %EA%B0%95%EB%8F%99%EC%97%AD
    #    강동역이란 한글 대신 URL로 변환하여 변환된 주소를 넣어줘야 한다.
    #    "https://www.diningcode.com/list.php?query=%EA%B0%95%EB%8F%99%EC%97%AD"

    url = "https://www.diningcode.com/list.php?query=" + urllib.parse.quote(station)
    browser = webdriver.Chrome("C:\\Users\kem\Desktop\crawling\scraping\chromedriver.exe")
    browser.get(url)
    try:
        more_view = browser.find_element_by_xpath('//*[@id="div_list_more"]')   # 페이지 내에서 식당들 더보기(요소)를 찾아서 변수에 저장
    except:
        print("식당 더보기 버튼이 없음")
        return
        
    interval = 0.5
    while True:       # 더보기 버튼을 눌러서 더 많은 식당을 볼 수 있도록 한다.
        try:
            more_view.click()
            time.sleep(interval)
        except:
            break

    soup = BeautifulSoup(browser.page_source, "lxml")


    # soup변수에는 검색한 지역의 전체 lxml문서가 저장되어 있고, 여기서 식당에 접근할 수 있는 링크들을 찾아야 한다.
    # class가 blink인 'a'태그에 정보들이 있으므로 soup.find_all() 함수를 이용해 class가 blink인 'a'태그를
    # 모두 찾아서 rank변수에 저장한다. 이 때 리스트 형식으로 저장된다.
    # 따라서, 각 식당에 rank[0] 식으로 접근할 수 있다.
    rank = soup.find_all("a", attrs={"class":"blink"}) 
    review_link = []


    # rank에는 각 식당의 간략한 정보와 식당에 대해 더 자세한 사항을 볼 수 있는, 페이지링크가 있다.
    # 원하는 데이터는 유저들의 리뷰이고, 리뷰는 식당 페이지에 있으므로
    # rank에서 식당의 링크를 추출하여 해당 식당 페이지로 가서 리뷰들을 추출해야 한다.
    for r in rank:
        if r['href'][0:8] == '/profile':                           
            link = "https://www.diningcode.com" + r['href']
            review_link.append(link)


    # 추출한 링크에 방문하여 리뷰(데이터)들을 가져온다.
    # f = open("review.csv", "w")
    for link in review_link:
        browser.get(link)
        # numberOfReview = 0

        # 리뷰의 개수를 찾아서 개수 만큼만 더보기 버튼 누르기
        try:
            numberOfReview = int(re.findall("\d+", browser.find_element_by_class_name('point').text)[0])
        except:
            browser.quit()
            browser = webdriver.Chrome("C:\\Users\kem\Desktop\crawling\scraping\chromedriver.exe")
            browser.get(link)
            try:
                numberOfReview = int(re.findall("\d+", browser.find_element_by_class_name('point').text)[0])
            except:
                continue


        if numberOfReview > 5:
            more_review = browser.find_element_by_id('div_more_review')   # 더보기 버튼 찾아서 변수에 저장
            while True:     # 더보기 버튼을 누를 때마다 5개의 리뷰가 추가 생성. 루프를 돌며 모든 리뷰를 볼 수 있게 함.
                try:
                    more_review.click()
                    time.sleep(interval)
                except:     # 리뷰를 모두 보여주면 더보기 버튼이 없어지는데, 이 때 click()을 호출하면 에러가 발생한다. 
                    break   # 에러가 발생하면 while문을 빠져 나오도록 한다.
        
        soup2 = BeautifulSoup(browser.page_source, "lxml")      # 페이지의 모든 내용을 가져온다.

        title = soup2.find("div", attrs={"class":"tit-point"}).get_text()      # 식당이름 가져오기
        address = soup2.find("li", attrs={"class":"locat"}).get_text()         # 식당 주소 
        score_list = soup2.find_all("p", attrs={"class":"point-detail"})            # 리뷰 점수(5점 만점)
        reviews = soup2.find_all("p", attrs={"class":"review_contents btxt"})  # 모든 리뷰 찾아서 저장
        empathy_list = soup2.find_all("div", attrs={"class":"symp-btn"})       # 공감수
        
        # 가져온 텍스트들의 개행문자 제거
        title = funcs.remove_space(title)
        address = funcs.remove_space(address)
        
        restaurant_dic[address] = restaurant_dic.get(address, 0)    # 식당의 주소를 기반으로 중복검사
        if restaurant_dic[address] == 1:
            continue
        restaurant_dic[address] = 1

        # 식당 특징
        feature = funcs.extract_feature(soup2.find("ul", attrs={"class":"app-arti"}).get_text())
        
        # 리뷰점수 추출
        score = []
        mean_score = funcs.extract_score(score_list[0].get_text())
        for i in range(1,len(score_list)):
            score.append(funcs.extract_score(score_list[i].get_text()))

        for i, review in enumerate(reviews):
            text = funcs.remove_space(review.get_text())
            empathy = funcs.extract_empathy(empathy_list[i].get_text())
            try:
                f.write(title + ',' + address + ',' + score[i] + ','+ empathy + ',' + feature + ',' + text + "\n")
            except IndexError:
                try:
                    f.write(title + ',' + address + ',' + mean_score + ','+ empathy + ',' + feature + ',' + text + "\n")
                except:
                    continue
            except UnicodeEncodeError:      # 리뷰에 이모티콘이나 인식할 수 없는 문자가 있어서 csv 파일에 쓸 수 없을 때
                    continue                    # 그 리뷰는 건너뛰고 계속한다.
            
    # f.close()
    browser.quit()



# #######################            test            ############################
# # res = requests.get(review_link[0])
# # res.raise_for_status()
# # soup2 = BeautifulSoup(res.text, "lxml")
# browser.get(review_link[0])

# #리뷰의 개수를 찾아서 개수 만큼만 더보기 버튼 누르기
# numberOfReview = int(re.findall("\d+", browser.find_element_by_class_name('point').text)[0])
# more_review = browser.find_element_by_id('div_more_review')   # 더보기 버튼 찾아서 변수에 저장
# count = 1
# while count*5 < numberOfReview:     # 더보기 버튼을 누를 때마다 5개의 리뷰가 추가 생성. 루프를 돌며 리뷰의 개수에 맞게 버튼 클릭
#     more_review.click()
#     time.sleep(interval)
#     count += 1

# soup2 = BeautifulSoup(browser.page_source, "lxml")

# title = soup2.find("div", attrs={"class":"tit-point"}).get_text()   # 식당이름 가져오기
# address = soup2.find("li", attrs={"class":"locat"}).get_text()      # 식당 주소 
# score = soup2.find("span", attrs={"class":"point"}).get_text()      # 리뷰 점수(5점 만점)
# reviews = soup2.find_all("p", attrs={"class":"review_contents btxt"})  # 모든 리뷰 찾아서 저장
# empathy_list = soup2.find_all("div", attrs={"class":"symp-btn"})    # 공감횟수

# # 가져온 텍스트들의 개행문자 제거
# title = funcs.remove_space(title)
# address = funcs.remove_space(address)
# score = funcs.remove_space(score)


# f = open("review.csv", "w")
# for i, review in enumerate(reviews):
#         text = funcs.remove_space(review.get_text())
#         empathy = funcs.extract_empathy(empathy_list[i].get_text())
#         try:
#             f.write(title + ',' + address + ',' + score + ',' + empathy + ',' + text + ',' +  "\n")
#         except UnicodeEncodeError:      # 리뷰에 이모티콘이나 인식할 수 없는 문자가 있어서 csv 파일에 쓸 수 없을 때
#             continue                    # 그 리뷰는 건너뛰고 계속한다.
# f.close()