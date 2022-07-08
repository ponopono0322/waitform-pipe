from abc import ABC
import pandas as pd
import chromedriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class chromedriver(ABC):

    # 생성자
    def __init__(self, debug=False):
        path = chromedriver_autoinstaller.install()  # 크롬 드라이버 설치 및 경로 반환
        options = webdriver.ChromeOptions()          # 크롬 옵션 추가
        if not debug:                                # 디버그 수행시 창 띄워서 진행
            options.add_argument("headless")         # 백그라운드 실행
            options.add_argument('no-sandbox')
            # options.add_argument("single-process")
            options.add_argument("disable-dev-shm-usage")
            options.add_argument("disable-gpu") 
            options.add_argument("--remote-debugging-port=9222")
        self.driver = webdriver.Chrome(
            service=Service(path), chrome_options=options)  # 크롬 브라우저 사용하기
        self.link_col = ['position', 'link', 'visited']     # 링크 데이터 열 정보
        self.data_col = ['position', 'data', 'visited']     # 공고문 데이터 열 정보
        self.linkdf = pd.DataFrame(columns=self.link_col)   # 링크 데이터프레임
        self.datadf = pd.DataFrame(columns=self.data_col)   # 공고문 데이터프레임

    # 추상 메소드
    @classmethod
    def getdata(self):
        pass

    # 추상 메소드
    @classmethod
    def getlink(self):
        pass

    # 새 데이터만 크롤링 할 수 있도록 하는 함수
    def datacheck(self, new_df, type='data'):
        if type == 'data':
            self.datadf = new_df
        else:
            self.linkdf = new_df

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
