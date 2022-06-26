from abc import ABC
import pandas as pd
import chromedriver_autoinstaller
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class chromedriver(ABC):

    # 생성자
    def __init__(self, debug=False):
        path = chromedriver_autoinstaller.install()         # 크롬 드라이버 설치 및 경로 반환
        options = webdriver.ChromeOptions()                 # 크롬 옵션 추가
        if not debug:                                       # 디버그 수행시 창 띄워서 진행
            options.add_argument("headless")                # 백그라운드 실행
        self.driver = webdriver.Chrome(
            service=Service(path), chrome_options=options)  # 크롬 브라우저 사용하기
        self.link_col = ['position', 'link', 'visited']     # 링크 데이터 열 정보
        self.data_col = ['position', 'data', 'visited']     # 공고문 데이터 열 정보
        self.linkdf = pd.DataFrame(columns=self.link_col)   # 링크 데이터프레임
        self.datadf = pd.DataFrame(columns=self.data_col)   # 공고문 데이터프레임

    # df -> csv 함수
    def exporttocsv(self, path, type='data'):
        if type == 'link':                                  # 링크 데이터 csv 저장
            self.linkdf.to_csv(path, index=False, encoding='utf-8')
        else:                                               # 공고문 데이터 csv 저장
            self.datadf.to_csv(path, index=False, encoding='utf-8')
    
    # 기존 데이터와 합치는 작업
    def mergecsv(self, path, before_df):
        if os.path.exists(path):                            # 경로에 기존 파일이 있다면
            new_df = pd.concat([pd.read_csv(path), before_df], ignore_index=True)
            new_df.to_csv(path, encoding='utf-8')           # 데이터를 합친 후 저장
        else:                                               # 기존 파일이 없다면
            before_df.to_csv(path, encoding='utf-8')        # 새 파일 만들기

    # 추상 메소드
    @classmethod
    def getdata(self):
        pass
    
    # 추상 메소드
    @classmethod
    def getlink(self):
        pass

    # 링크 데이터 열 정보 반환
    def getlinkcol(self):
        return self.link_col
    
    # 공고문 데이터 열 정보 반환
    def getdatacol(self):
        return self.data_col

    # 페이지 갱신 대기
    def waiting(self, time=60):
        self.driver.implicitly_wait(time_to_wait=time)

    # 크롬 드라이버 닫는 함수
    def close(self):
        self.driver.close()

    # 크롬 드라이버 종료 함수
    def quit(self):
        self.driver.quit()