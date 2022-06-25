import pandas as pd
import chromedriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class chromedriver:

    # 생성자
    def __init__(self, debug=False):                    
        path = chromedriver_autoinstaller.install()     # 크롬 드라이버 설치 및 경로 반환
        options = webdriver.ChromeOptions()             # 크롬 옵션 추가
        if not debug:                                   # 디버그 수행시 창 띄워서 진행
            options.add_argument("headless")            # 백그라운드 실행

        self.driver = webdriver.Chrome(service=Service(path), chrome_options=options)    # 크롬 브라우저 사용하기
        self.linkdf = pd.DataFrame(columns=['position', 'link'])    # 링크 데이터 저장
        self.datadf = pd.DataFrame(columns=["position", "data"])    # 공고문 데이터 저장
     
    # df -> csv 함수
    def exporttocsv(self, path, type='data'):
        if type == 'link':                              # 링크 데이터 csv 저장
            self.linkdf.to_csv(path, index=False, encoding='utf-8')
        else:                                           # 공고문 데이터 csv 저장
            self.datadf.to_csv(path, index=False, encoding='utf-8')

    # link -> data 함수
    def getdata(self):
        for pos, URL in zip(self.linkdf['position'], self.linkdf['link']):
            self.driver.get(URL)
            self.driver.implicitly_wait(time_to_wait=60)
            try:
                data = self.driver.find_element(By.CLASS_NAME, "JobContent_descriptionWrapper__SM4UD")
            except:
                data = None
            tmp = pd.DataFrame([[pos, data.text]], columns=['position', 'data'])
            self.datadf = pd.concat([self.datadf, tmp], ignore_index=True)

    # 크롬 드라이버 닫는 함수
    def close(self):
        self.driver.close()
        
    # 크롬 드라이버 종료 함수
    def quit(self):
        self.driver.quit()