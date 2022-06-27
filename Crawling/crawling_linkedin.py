from ast import excepthandler
from operator import index
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import pandas as pd

# https://www.linkedin.com/jobs/search/?currentJobId=10000&geoId=103644278&keywords=database&location=%EB%AF%B8%EA%B5%AD


driver = webdriver.Chrome('chromedriver')  # https://chromedriver.chromium.org/downloads
driver.implicitly_wait(10)
# 로그인 페이지로 이동
URL = 'https://www.linkedin.com/login/ko?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
driver.get(url=URL)
driver.implicitly_wait(5)
# 3091327134 3084008208 3092650694 3083077458 3089270328 3090144106 3089661302 3072802817 3083678124 3083640103
# 로그인
driver.find_element_by_id('username').send_keys('tpqls3141@gmail.com') # ID 입력
driver.find_element_by_id('password').send_keys('tpqls3141!') # PW 입력
search_btn = driver.find_element_by_css_selector('#organic-div > form > div.login__form_action_container > button') # button element
search_btn.click()
# print('login done!!!!!!!!!!!!!!!!!!!')

hashtag = ['backend%20developer','software','system','database','network','Frontend%20Developer','Application','Service','Game%20Developer','AI%20Engineer'] 
baseUrl = 'https://www.linkedin.com/jobs/search/?currentJobId='
midUrl = '&geoId=103644278&keywords='
tailUrl = '&location=%EB%AF%B8%EA%B5%AD'    # 0~975 그 이상도 가능

url1 = 'https://www.linkedin.com/jobs/search/?geoId=103644278&keywords='
url2 = '&location=미국&start='

# 크롤링 url 탐색
code_lists = []
for h in hashtag[7:]:
    code_list = []
    for i in range(0,975,25):   #975
        URL = url1 + h + url2 + str(i)
        print(URL)
        driver.get(url=URL)
        driver.implicitly_wait(10)  

        try:
            for item in driver.find_elements_by_css_selector("body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__left-rail > div > div > ul > li"):
                code = item.get_attribute('data-occludable-job-id')
                print(code)
                code_list.append(code)
                
                data = {
                    'code' : code,
                    'hashtag' : h
                }

                with open('./code.csv', 'a', encoding='utf-8', newline='') as csvfile:
                    fieldnames = ['code', 'hashtag']
                    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    csvwriter.writerow(data)
        except:
            print('error2')
            continue

    code_lists.append(code_list)           
print('찾은 코드 컬럼수:', len(code_lists))
print('컴럼 하나당 코드수:', len(code_lists[0]))

df = pd.read_csv('code.csv', encoding='utf-8')
df = pd.DataFrame(df)
df.dropna()

# print(df.iloc[:1])

# for i in range(len(df)):
#     c = df.loc[i, "code"]
#     print(type(c))
#     print(c)
#     print(int(c))
#     print(type(c))
#     print(df.loc[i, "hash"])

# 크롤링 시작
cnt = 1
for h in hashtag[:2]:    
    for i in range(len(df)):    
        try:
            c = df.loc[i, "code"]
            c = int(c)
            h = df.loc[i, 'hash']
            try:
                # Search Keyword
                URL = baseUrl + str(c) + midUrl + h + tailUrl
                print(URL, end='\n')
                driver.get(url=URL)
                driver.implicitly_wait(10)             
                item = driver.find_elements_by_xpath("//*[@id='main']/div/section[2]/div/div[2]/div[1]/div/div[2]")
                content = item[0].text   
                print(content)  
# /html/body/div[5]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[2]
                rinkedin_data = {
                    'content' : content,
                    'tag' : h
                }

                with open('./code_data.csv', 'a', encoding='utf-8', newline='') as csvfile:
                    fieldnames = ['content', 'tag']
                    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    csvwriter.writerow(rinkedin_data)

                print(cnt, "번째 성공")
                cnt +=1
                time.sleep(3)
                
            except:
                print("error1!!")
                continue 

        except:
            print("error2!!")
            continue
        
print('crwaling clear!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
# print('총데이터: ',cnt,'개')
driver.close()
