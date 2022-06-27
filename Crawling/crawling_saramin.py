
from urllib.request import Request, urlopen, HTTPError
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import csv

# Back_end 161 : https://www.saramin.co.kr/zf_user/jobs/list/job-category?page=1&cat_kewd=87%2C88%2C84%2C194%2C93%2C94%2C115%2C113%2C2232&search_optional_item=n&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle
# Software 22 : https://www.saramin.co.kr/zf_user/jobs/list/job-category?page=2&cat_kewd=192%2C184&search_optional_item=n&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle
# System 9 : https://www.saramin.co.kr/zf_user/jobs/list/job-category?page=2&cat_kewd=319%2C185%2C186%2C189%2C320&search_optional_item=n&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle
# Database 27 : https://www.saramin.co.kr/zf_user/jobs/list/job-category?page=2&cat_kewd=83%2C192%2C191%2C110&search_optional_item=n&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle
# Network/Security 75 : https://www.saramin.co.kr/zf_user/jobs/list/job-category?page=2&cat_kewd=85%2C90%2C104%2C111%2C114%2C190%2C193%2C112&search_optional_item=n&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle
# Front_end 87 : https://www.saramin.co.kr/zf_user/jobs/list/job-category?page=2&cat_kewd=92%2C91&search_optional_item=n&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle
# Application 40 : https://www.saramin.co.kr/zf_user/jobs/list/job-category?page=2&cat_kewd=112%2C195&search_optional_item=n&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle
# Service 108 : https://www.saramin.co.kr/zf_user/jobs/list/job-category?page=2&cat_kewd=89%2C81&search_optional_item=n&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle
# Game 9 : https://www.saramin.co.kr/zf_user/jobs/list/job-category?page=2&cat_kewd=80&search_optional_item=n&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle
# AI 58 : https://www.saramin.co.kr/zf_user/jobs/list/job-category?page=2&cat_kewd=82%2C105%2C106%2C107%2C108%2C109%2C116&search_optional_item=n&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle

base_url = 'https://www.saramin.co.kr/zf_user/jobs/list/job-category?page='
url_list = ['&cat_kewd=87%2C88%2C84%2C194%2C93%2C94%2C115%2C113%2C2232','&cat_kewd=192%2C184','&cat_kewd=319%2C185%2C186%2C189%2C320','&cat_kewd=83%2C192%2C191%2C110','&cat_kewd=85%2C90%2C104%2C111%2C114%2C190%2C193%2C112','&cat_kewd=92%2C91','&cat_kewd=112%2C195','&cat_kewd=89%2C81','&cat_kewd=80','&cat_kewd=82%2C105%2C106%2C107%2C108%2C109%2C116']
url_list2 = ['&cat_kewd=83%2C192%2C191%2C110','&cat_kewd=85%2C90%2C104%2C111%2C114%2C190%2C193%2C112','&cat_kewd=92%2C91','&cat_kewd=112%2C195','&cat_kewd=89%2C81','&cat_kewd=80','&cat_kewd=82%2C105%2C106%2C107%2C108%2C109%2C116']
tail_url = '&search_optional_item=n&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
num_list = [161,22,9,27,75,87,40,108,9,58]
num_list2 = [27,75,87,40,108,9,58]
data = [[]for _ in range(7)]           # url 저장 리스트

# 각 해쉬태그의 url들을 찾는 크롤링코드
driver = webdriver.Chrome("chromedriver")
for idx, num in enumerate(num_list2):  
    for n in range(1, num+1):
        URL = base_url + str(n) + url_list2[idx] + tail_url
        driver.get(url=URL)
        driver.implicitly_wait(time_to_wait=60)

        div = driver.find_elements(By.CLASS_NAME, "list_item")
        for item in div:
            tmp = item.find_element(By.TAG_NAME, "a").get_attribute('href')
            data[idx].append(tmp)
        time.sleep(2)
        
driver.close()
print('step1 done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print(len(data))

hashtag = ['Back_end', 'Software', 'System', 'Database', 'Network/Security', 'Front_end', 'Application', 'Service', 'Game', 'AI']
hashtag2 = ['Database', 'Network/Security', 'Front_end', 'Application', 'Service', 'Game', 'AI']
counting = 0

driver = webdriver.Chrome("chromedriver")
for idx in range(len(data)):
    for url in data[idx]:
        try:
            driver.get(url=url)
            driver.implicitly_wait(time_to_wait=60)
            try:
                driver.switch_to.frame("iframe_content_0")
                contents = driver.find_element(By.CLASS_NAME, "user_content").text
                
                saramin_data = {
                'content' : contents,
                'tag' : hashtag2[idx]
                }  

                with open('./saramin_data.csv', 'a', encoding='utf-8', newline='') as csvfile:
                    fieldnames = ['content', 'tag']
                    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    csvwriter.writerow(saramin_data)

                counting += 1   
                print(counting,'번째 : ', hashtag[idx])     
                time.sleep(2)

            except:
                continue
        except:
            continue

driver.close()
print('step2 done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print('총데이터:', counting, '개')
