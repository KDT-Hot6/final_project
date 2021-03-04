from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import re

next_page_num1 = int(input("현재 페이지를 지정해주어야함:"))
check_max = int(input("내가 시작하고 싶은 음식점 순서를 정해줘!! index는 1부터!!")) - 1
check = 0


"""
summary
just for one page.
so need to contain total pages and that of the entire reviews of the each restaurant
"""

# start tripadvisor_seoul
options = webdriver.ChromeOptions()
options.add_argument('window-size=1080, 720')

driver = webdriver.Chrome('chromedriver', options=options)
driver.implicitly_wait(5)
driver.get(url='https://www.tripadvisor.co.kr/Restaurants-g294197-Seoul.html')
sleep(5)

# set page
if next_page_num1 != 1:
    next_page = driver.find_element_by_link_text("{}".format(next_page_num1))
    ActionChains(driver).key_down(Keys.LEFT_CONTROL).click(next_page).key_up(Keys.LEFT_CONTROL).perform()
    driver.implicitly_wait(5)
    sleep(3)
next_page_num1 += 1

# find a restaurant_list at the page
try:
    while True:
        click_box_list = driver.find_elements_by_class_name('_1llCuDZj')
        for click_box in click_box_list:
            if check < check_max:
                check += 1
                continue
            click_box = click_box.find_element_by_class_name('_2Hb-Mt7l')
            ActionChains(driver).key_down(Keys.LEFT_CONTROL).click(click_box).key_up(Keys.LEFT_CONTROL).perform()
            last_tab = driver.window_handles[-1]
            driver.switch_to.window(window_name=last_tab)
            driver.implicitly_wait(5)
            sleep(3)

            # the information of the restaurant
            res_name = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[3]/div/div/div[1]/h1').text
            try: res_phone = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[3]/div/div/div[3]/span[2]/span/span[2]/a').text
            except: res_phone = ""
            res_address = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[3]/div/div/div[3]/span[1]/span/a').text
            res_point = float(driver.find_element_by_class_name('r2Cf69qf').text)
            try: res_food_type = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[3]/div/div/div[2]/span[3]/a[2]').text
            except: res_food_type = ""
            driver.implicitly_wait(5)

            with open("advisor_seoul_res_new.csv", 'a', encoding='utf-8') as f:
                f.write('{}, {}, {}, {}, {}\n'.format(res_name, res_phone, res_address, res_food_type, res_point))

            try:
                next_page_num2 = 2
                while True:
                    # see full contents of reviews
                    # full_review = driver.find_elements_by_xpath('//span[contains(text(), "더 보기")]')
                    full_review = driver.find_elements_by_xpath('//span[text()="더 보기"]')
                    driver.implicitly_wait(5)
                    sleep(3)
                    ActionChains(driver).move_to_element(full_review[0]).click().perform()
                    driver.implicitly_wait(5)
                    sleep(3)
                    # collect reviews(yet just 1page)
                    review_list = driver.find_elements_by_class_name('reviewSelector')
                    driver.implicitly_wait(5)
                    sleep(2)
                    for review in review_list:
                        rev_create_date = review.find_element_by_class_name('ratingDate').text

                        # hangul = re.compile('[^ㄱ-ㅣ가-힣0-9 ]+')
                        # rev_comment = hangul.sub(" ", review.find_element_by_class_name('partial_entry').text)
                        try: rev_comment = re.sub(pattern=r'[,\n]+', repl=' ',
                                                  string=review.find_element_by_class_name('partial_entry').text)
                        except: continue

                        review_class = review.get_attribute("innerHTML") ### 이걸로 하면된다.
                        review_point = re.search('\d+', re.search('ui_bubble_rating bubble_[0-9]+', review_class)[0])[0]

                        with open("advisor_seoul_review_new.csv", 'a', encoding='utf-8') as f:
                            f.write('{}, {}, {}, {}, {}\n'.format(res_name, res_phone, rev_create_date, rev_comment, review_point))
                        # go to next page
                        sleep(1)
                    sleep(3)
                    next_page = driver.find_element_by_link_text("{}".format(next_page_num2))
                    ActionChains(driver).key_down(Keys.LEFT_CONTROL).click(next_page).key_up(Keys.LEFT_CONTROL).perform()
                    driver.implicitly_wait(5)
                    sleep(3)
                    next_page_num2 += 1
            except Exception as f:
                print(f)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print("끝난 가게명: {}".format(res_name))

        next_page = driver.find_element_by_link_text("{}".format(next_page_num1))
        ActionChains(driver).key_down(Keys.LEFT_CONTROL).click(next_page).key_up(Keys.LEFT_CONTROL).perform()
        print("현재 페이지: {}".format(next_page_num1))
        driver.implicitly_wait(5)
        sleep(3)
        next_page_num1 += 1
except Exception as f:
    print(f)