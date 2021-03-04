import sys
sys.path.insert(0,'.')
import mysql_auth
import pymysql
import re
from selenium import webdriver

#기본 설정
login = mysql_auth.info

hot6_db = pymysql.connect(
    user = login['user'],
    passwd = login['passwd'],
    host = login['host'],
    db = login['db'],
    charset = login['charset']
)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

BASE_URL = 'https://www.mangoplate.com/search/'
keyword = ''

# 검색할 단어 초기화하기
def set_keyword(word):
  global keyword
  keyword = word

# 해당 검색어의 페이지 수를 반환
def get_page_number():
  print(keyword,"검색중 ...")
  driver.get(BASE_URL+keyword)
  print(keyword,"검색완료")
  time.sleep(2)
  a_tags = driver.find_elements_by_css_selector('.paging > a')
  page_number = len(a_tags)
  print(keyword, "페이지 수", page_number)
  return page_number

# 페이지로 이동하기 - 페이지를 입력받아 해당 페이지로 이동
def go_to_page(page_num):
  print(page_num,"페이지로 이동중")
  driver.get(BASE_URL+keyword+'?keyword='+keyword+'&page='+str(page_num))
  print(page_num,"페이지로 이동 완료")

# 페이지 내의 가게 개수 반환    
def get_page_restaurant_number():
  print("페이지 내의 가게 리스트 생성중")
  list_restaurant_items =driver.find_elements_by_css_selector('.server_render_search_result_item > .list-restaurant-item')
  print(len(list_restaurant_items),"가게 리스트 생성 완료")
  return len(list_restaurant_items)

# 가게 페이지로 이동
def go_to_restaurant_page(index):
  print(index+1,"가게로 이동중")
  driver.find_elements_by_css_selector('.server_render_search_result_item > .list-restaurant-item')[index].click()
  time.sleep(3)
  print(index+1,"가게로 이동 완료")

# 가게의 총 리뷰 개수 얻기
def get_total_review_number():
  print("가게의 총 리뷰 개수 얻는중")
  cnt_review = driver.find_element_by_css_selector('.review').text
  print("가게의 총 리뷰 개수 :",cnt_review)
  return cnt_review

# 현재 페이지 내의 리뷰 개수 얻기
def get_page_review_number():
  print("현재 페이지의 리뷰 개수 파악중")
  review_list = driver.find_elements_by_css_selector('li.RestaurantReviewList__ReviewItem')
  page_review_number = len(review_list)
  print("현재 페이지 리뷰 개수",page_review_number)
  return page_review_number

# 리뷰 저장
def save_review_info(index,res_id):
  user_name = driver.find_elements_by_css_selector('.RestaurantReviewItem__UserNickName')[index].text.replace("\'","\\'")
  user_review = ''.join(re.findall("\d",driver.find_elements_by_css_selector('.RestaurantReviewItem__UserStatItem--Review')[index].text))
  user_follower = ''.join(re.findall("\d",driver.find_elements_by_css_selector('.RestaurantReviewItem__UserStatItem--Follower')[index].text))
  date = driver.find_elements_by_css_selector('.RestaurantReviewItem__ReviewDate')[index].text.replace("\'","\\'")
  comment = driver.find_elements_by_css_selector('.RestaurantReviewItem__ReviewText')[index].text.replace("\'","\\'")
  star = driver.find_elements_by_css_selector('.RestaurantReviewItem__RatingText')[index].text
  if star == '맛있다':
    star = 3
  elif star == '괜찮다':
    star = 2
  elif star == '별로':
    star = 1
  else:
    star = 0

  sql = '''
    INSERT INTO `REVIEW` 
    (`REV_USER_NAME`,`REV_USER_REV`,`REV_USER_FOLLOWER`,`REV_CREATE_DATE`,`REV_COMMENT`,`REV_POINT`,`SITE_ID`,`RES_ID`) 
    VALUES ('{0}',{1},{2},'{3}','{4}',{5},2,{6})
  '''.format(user_name,user_review,user_follower,date,comment,star,res_id)
  
  cursor.execute(sql)
  print(index +1,"번째 리뷰 저장 완료 - 커밋전")

# 더보기 버튼 클릭
def get_more_review():
  print("더보기 버튼 클릭")
  element = driver.find_element_by_css_selector('.RestaurantReviewList__MoreReviewButton')
  driver.execute_script("arguments[0].click();", element)
  time.sleep(2)
  print("더보기 버튼 클릭완료")

# 식당 정보 저장 - 저장 후 인덱스 반환
def save_restaurant_info(res_dic):
  sql = get_restaurant_insert_sql(res_dic)  
  cursor.execute(sql)
  print("식당 저장 완료 - 커밋 전")
  return cursor.lastrowid  

# 페이지 뒤로 가기 (한 음식점 리뷰를 모두 모았으면 다시 음식점 리스트 페이지로 돌아감)
def go_back_page():
    print('페이지 돌아가기중')
    driver.execute_script("window.history.go(-1)")
    time.sleep(5)
    print('페이지 돌아가기 완료')

# 사이트 데이터 키를 조회한다.
def get_site_data_key(table_name):
  sql = 'SELECT * FROM `SITE_DATA_KEY` WHERE SITE_ID = 2 AND SDK_TB=\'{}\''.format(table_name)
  cursor.execute(sql)
  result = cursor.fetchall()
  return result

# 조회된 사이트 데이터 키를 바탕으로 데이터가 존재하는지 확인한다.
def check_data(index,rows,col_list,val_list):
  sdk_key =  driver.find_element_by_css_selector('tbody > tr:nth-child('+str(index+1)+') > th').text
  for row in rows:
    if row['SDK_KEY'] == sdk_key:
      col_list.append(row['SDK_COL'])
      if sdk_key == '웹 사이트':
        val_list.append(driver.find_element_by_css_selector('tbody > tr:nth-child('+str(index+1)+') > td > a').get_attribute('href').replace("\'","\\'"))
      else: 
        val_list.append(driver.find_element_by_css_selector('tbody > tr:nth-child('+str(index+1)+') > td').text)
      rows.remove(row)
      break

# 식당 정보가 들어있는 table row 개수 확인
def get_restaurant_info_cnt():
  info_list = driver.find_elements_by_css_selector('tbody > tr')
  return len(info_list)

# 식당 정보를 바탕으로 insert query를 동적으로 생성한다.
def get_restaurant_insert_sql(res_dic):
  sql = 'INSERT INTO `RESTAURANT` '+ str(col_list).replace('\'','`').replace('[','(').replace(']',') VALUES ') + str(val_list).replace('[','(').replace(']',')')
  return sql

# 식당이 가지고 있는 데이터를 딕셔너리로 반환
def get_restaurant_info():
  info_cnt = get_restaurant_info_cnt()
  rows = get_site_data_key('RESTAURANT') 
  col_list = []
  val_list = []
  for i in range(info_cnt):
    check_data(i,rows,col_list,val_list)
  
  RES_NAME = driver.find_element_by_css_selector('.restaurant_name').text.replace("\'","\\'")
  col_list.append('RES_NAME')
  val_list.append(RES_NAME)
  
  RES_POINT = '-1' # 식당 point 존재하지 않으면 -1
  try:
    RES_POINT = driver.find_element_by_css_selector('strong.rate-point > span').text
  except Exception as e:
    print(e)
  col_list.append('RES_POINT')
  val_list.append(RES_POINT)
  
  RES_REV = ''.join(re.findall("\d",driver.find_element_by_css_selector('.review').text))
  col_list.append('RES_REV')
  val_list.append(RES_REV)

  RES_HIT = ''.join(re.findall("\d",driver.find_element_by_css_selector('.hit').text))
  col_list.append('RES_HIT')
  val_list.append(RES_HIT)

  RES_FAVORITE = ''.join(re.findall("\d",driver.find_element_by_css_selector('span.favorite').text))
  col_list.append('RES_FAVORITE')
  val_list.append(RES_FAVORITE)
  return dict(zip(col_list, val_list))

# 같은 주소의 식당이 있는지 확인
def find_restaurant_for_address(address):
  sql = 'SELECT * FROM RESTAURANT WHERE RES_ADDRESS = \'{}\''.format(address)
  return cursor.execute(sql)

#DB 커서 초기화
cursor = hot6_db.cursor(pymysql.cursors.DictCursor)

# 드라이버 생성
driver = webdriver.Chrome('chromedriver',options=options)
driver.implicitly_wait(10) 

# 크롤링 실행 코드
set_keyword('홍대입구역')
page_cnt = get_page_number()
for k in range(1,page_cnt+1):
  go_to_page(k)
  cnt_restaurant = get_page_restaurant_number()
  for j in range(cnt_restaurant):
    go_to_restaurant_page(j)
    res_dic = get_restaurant_info()
    rev_cnt = int(res_dic['RES_REV'])
    affected_row = find_restaurant_for_address(red_dic['RES_ADDRESS'])
    if affected_row > 0 or rev_cnt == 0:
        print("같은 식당 존재하거나 리뷰가 존재하지 않는 식당")
        go_back_page()
        continue
    res_id = save_restaurant_info(res_dic)
    for i in range(rev_cnt):
      if i > 4 and i%5 == 0:
        get_more_review()
      try:
        save_review_info(i,res_id)
      except Exception as e: #크롤링해서 얻은 리뷰 수와 실제 리뷰수의 차이로 발생되는 에러
        print(e)
        remove_review_cnt = cnt_review - i
        print("삭제된 리뷰의 개수",remove_review_cnt)
        sql = "UPDATE `RESTAURANT` SET `RES_DEL_REV` = {0} WHERE `RES_ID` = {1}".format(remove_review_cnt,res_id)
        cursor.execute(sql)
        break    
    go_back_page()
    hot6_db.commit()
    print('커밋완료')
hot6_db.close()
driver.close()