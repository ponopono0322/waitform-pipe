from abc import ABC
import pandas as pd
import chromedriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class chromedriver(ABC):

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
    
    # 추상 메소드
    @classmethod
    def getdata(self):
        pass
    
    # 추상 메소드
    @classmethod
    def getlink(self):
        pass

    # 페이지 갱신 대기
    def waiting(self, time=60):
        self.driver.implicitly_wait(time_to_wait=time)

    # 크롬 드라이버 닫는 함수
    def close(self):
        self.driver.close()

    # 크롬 드라이버 종료 함수
    def quit(self):
        self.driver.quit()