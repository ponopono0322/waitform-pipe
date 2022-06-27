# 2022.04.06 4:38 programmers crawling done!
# 'stack'부분과 position, requirements, preference 부분을 'content'로 묶고 'tag'(해쉬태그)부분을 추가해 총 3개의 컬럼으로 구성한 csv파일의 크롤링코드
# 총 데이터: '3263'개

from urllib.request import Request, urlopen, HTTPError
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import csv

# Back_end 52 : https://programmers.co.kr/job?page=1&job_category_ids=1&job_category_ids=6&job_category_ids=25&order=recent
# Software 7 : https://programmers.co.kr/job?page=1&job_category_ids=17&order=recent
# System 12 : https://programmers.co.kr/job?page=1&job_category_ids=18&job_category_ids=26&job_category_ids=27&job_category_ids=59&job_category_ids=13&order=recent
# Database 11 : https://programmers.co.kr/job?page=1&job_category_ids=12&order=recent
# Network/Security 12 : https://programmers.co.kr/job?page=1&job_category_ids=9&job_category_ids=22&order=recent
# Front_end 30 : https://programmers.co.kr/job?page=1&job_category_ids=4&order=recent
# Application 17 : https://programmers.co.kr/job?page=1&job_category_ids=2&job_category_ids=3&order=recent
# Service 4 : https://programmers.co.kr/job?page=1&job_category_ids=10&order=recent
# Game 6 : https://programmers.co.kr/job?page=1&job_category_ids=7&job_category_ids=16&job_category_ids=20&order=recent
# AI 18 : https://programmers.co.kr/job?page=1&job_category_ids=5&job_category_ids=11&job_category_ids=12&order=recent

base_url = 'https://programmers.co.kr/job?page='
url_list = ['&job_category_ids=1&job_category_ids=6&job_category_ids=25','&job_category_ids=17','&job_category_ids=18&job_category_ids=26&job_category_ids=27&job_category_ids=59&job_category_ids=13','&job_category_ids=12','&job_category_ids=9&job_category_ids=22','&job_category_ids=4','&job_category_ids=2&job_category_ids=3','&job_category_ids=10','&job_category_ids=7&job_category_ids=16&job_category_ids=20','&job_category_ids=5&job_category_ids=11&job_category_ids=12']
tail_url = '&order=recent'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
num_list = [52,7,12,11,12,30,17,4,6,18]
data = [[]for _ in range(10)]           # url 저장 리스트

# 각 해쉬태그의 url들을 찾는 크롤링코드
driver = webdriver.Chrome("chromedriver")
for idx, num in enumerate(num_list):  
    for n in range(1, num+1):
        URL = base_url + str(n) + url_list[idx] + tail_url
        driver.get(url=URL)
        driver.implicitly_wait(time_to_wait=60)

        div = driver.find_elements(By.CLASS_NAME, "list-position-item")
        for item in div:
            tmp = item.find_element(By.TAG_NAME, "a").get_attribute('href')
            data[idx].append(tmp)
        time.sleep(2)
        
driver.close()
print('step1 done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

# 각 url 크롤링
hashtag = ['Back_end', 'Software', 'System', 'Database', 'Network/Security', 'Front_end', 'Application', 'Service', 'Game', 'AI']
counting = 0

driver = webdriver.Chrome("chromedriver")
for idx in range(len(data)):
    for url in data[idx]:
        driver.get(url=url)
        driver.implicitly_wait(time_to_wait=60)
        try:
            stacks = driver.find_elements(By.TAG_NAME, "code")
            stack_data = []
            for stack in stacks:
                s = stack.text
                stack_data.append(s)

            position = driver.find_element(By.CLASS_NAME, "section-position")
            requirements = driver.find_element(By.CLASS_NAME, "section-requirements")
            preference = driver.find_element(By.CLASS_NAME, "section-preference")

            content = position.text + requirements.text + preference.text

            programmers_data = {
            'stack' : stack_data,
            'content' : content,
            'tag' : hashtag[idx]
            }  

            with open('./programmers_data.csv', 'a', encoding='utf-8', newline='') as csvfile:
                fieldnames = ['stack', 'content', 'tag']
                csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                csvwriter.writerow(programmers_data)

            counting += 1   
            print(counting,'번째 : ', stack_data)     
            time.sleep(3)

        except:
            continue

driver.close()
print('step2 done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print('총데이터:', counting, '개')
