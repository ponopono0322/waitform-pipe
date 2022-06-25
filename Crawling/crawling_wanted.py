import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import chromedriver_autoinstaller


def getlink():
    path = chromedriver_autoinstaller.install()     # 크롬 드라이버 설치 및 경로 반환
    options = webdriver.ChromeOptions()             # 크롬 옵션 추가
    options.add_argument("headless")                # 백그라운드 실행

    driver = webdriver.Chrome(service=Service(path), chrome_options=options)    # 크롬 브라우저 사용하기

    URL = "https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=company.response_rate_order&years=-1&locations=all"

    columns = {
        "Backend": ['웹 개발자', 'Node.js 개발자', 'PHP 개발자', '블록체인 플랫폼 엔지니어',
         'CTO,Chief Technology Officer'],
         "Software": ['소프트웨어 엔지니어', '자바 개발자', '파이썬 개발자', 'C,C++ 개발자',
         '.NET 개발자'],
         "System": ['DevOps / 시스템개발자', '시스템,네트워크 개발자', '임베디드 개발자',
         '하드웨어 개발자'],
         "DataBase": ['데이터 엔지니어', 'DBA'],
         "Network/Security": ['서버 개발자', '시스템,네트워크 개발자', '보안 엔지니어'],
         "Frontend": ['프론트엔드 개발자', '웹 퍼블리셔'],
         "Application": ['안드로이드 개발자', 'iOS 개발자', '크로스플랫폼 앱 개발자'],
         "Service": ['개발 매니저', 'QA,테스트 엔지니어', '기술지원', '프로덕트 매니저',
         'ERP전문가', 'CIO,Chief Information Officer'],
         "Game": ['VR 엔지니어'],
         "AI": ['머신러닝 엔지니어', '데이터 사이언티스트', '빅데이터 엔지니어', 'BI 엔지니어']
    }

    df = pd.DataFrame(columns=['position', 'link'])    

    for c_name, p_name in columns.items():
        driver.get(URL)
        driver.implicitly_wait(time_to_wait=60)

        dr = driver.find_element_by_class_name("JobCategory_JobCategory__btn__k3EFe")
        dr.click()
        time.sleep(0.5)

        for position in p_name:
            for i in driver.find_elements_by_tag_name('button'):
                if i.text == position:
                    i.click()
        
        tg = driver.find_element_by_class_name("Button_Button__label__1Kk0v").find_element_by_xpath("..")
        tg.click()

        time.sleep(1)
        df = scroll(df, c_name, driver)
        print(df)
    
    driver.close()
    driver.quit()


def scroll(df, pos, driver):
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
    
    time.sleep(1)
    div = driver.find_elements(By.CLASS_NAME, "Card_className__u5rsb")

    for item in div:
        link = item.find_element(By.TAG_NAME, "a").get_attribute('href')
        tmp = pd.DataFrame([[pos, link]], columns=['position', 'link'])
        df = pd.concat([df, tmp], ignore_index=True)

    return df

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