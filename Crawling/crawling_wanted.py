import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support.select import Select

def getlink():
    path = Service("/Users/shin/chromedriver")
    driver = webdriver.Chrome(service=path) #크롬 브라우저 사용

    URL = "https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=company.response_rate_order&years=-1&locations=all"
    driver.get(URL)
    driver.implicitly_wait(time_to_wait=60)

    df = pd.DataFrame()

    # 스크롤 내리기 이동 전 위치
    scroll_location = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 현재 스크롤의 가장 아래로 내림 
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") 
        # 전체 스크롤이 늘어날 때까지 대기 
        time.sleep(2) 
        # 늘어난 스크롤 높이 
        scroll_height = driver.execute_script("return document.body.scrollHeight") 
        # 늘어난 스크롤 위치와 이동 전 위치 같으면(더 이상 스크롤이 늘어나지 않으면) 종료 
        if scroll_location == scroll_height:
            break 
        # 같지 않으면 스크롤 위치 값을 수정하여 같아질 때까지 반복 
        else: # 스크롤 위치값을 수정
            scroll_location = driver.execute_script("return document.body.scrollHeight")
        break
            
    div = driver.find_elements(By.CLASS_NAME, "Card_className__u5rsb")
    for item in div:
        link = item.find_element(By.TAG_NAME, "a").get_attribute('href')
        tmp = pd.DataFrame([link])
        df = pd.concat([df, tmp])
        
    driver.close()

    df.to_csv('Book.csv', index=False)

def getdata():
    path = Service("/Users/shin/chromedriver")
    driver = webdriver.Chrome(service=path)

    df = pd.DataFrame(columns=["header", "detail"])

    for URL in df_link['link']:
        
        driver.get(URL)
        driver.implicitly_wait(time_to_wait=60)

        header = driver.find_element(By.CLASS_NAME, "JobHeader_className__HttDA")
        detail = driver.find_element(By.CLASS_NAME, "JobContent_descriptionWrapper__SM4UD")

        tmp = pd.DataFrame({"header":[header.text],
                            "detail":[detail.text]})
        df = pd.concat([df, tmp])
        time.sleep(1)
        
    driver.close()