import time
import pandas as pd

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from ChromeDriver import chromedriver

class Incruit(chromedriver):

    # 생성자
    def __init__(self, url, debug=False):
        super().__init__(debug)
        self.URL = url
        self.columns = {                        # 컬럼 사전 정의
            "Backend": ['웹프로그래머'],
            "Software": ['응용프로그래머'],
            "System": ['시스템프로그래머'],
            "DataBase": ['데이터베이스·DBA'],
            "Network/Security": ['네트워크·서버·보안'],
            "Frontend": ['웹디자인'],
            "Application": ['통신·모바일'],
            "Service": ['전산·IT기술지원'],
            "Game": ['게임(Game)'],
            "AI": ['빅데이터·AI(인공지능)']
        }

    # 링크 데이터 함수
    def getlink(self):
        for c_name, p_name in self.columns.items():         # 컬럼 사전으로부터 데이터 크롤링 시도
            self.driver.get(self.URL)                       # 원티드 사이트 개발자 주소
            self.waiting()                      # 사이트 갱신 대기

            for position in p_name:             # 사전 value 값 가져오기
                for i in self.driver.find_elements(By.TAG_NAME, "span"):  # 버튼 태그 목록 가져와서
                    if i.text == position:      # 사전 value 값과 비교
                        tg = i.find_element(By.XPATH, "..")
                        tg.click()              # 같다면 선택하기
                        break
                        
            time.sleep(1)
            sh = self.driver.find_element(By.ID, "SearchResultCount")   # 조건 검색하기 버튼
            sh.send_keys(Keys.ENTER)            # 선택된 태그로 검색하기     
            
            n_btn = True                        # 첫 페이지는 무조건 있으므로
            while n_btn:                        # 다음 페이지가 없을 때까지 반복
                self.nextpage(c_name)           # 다음 페이지 데이터 저장
                n_btn = self.isnext()           # 다음 페이지 넘기기

                if n_btn:                       # 다음 페이지가 있다면
                    n_btn.click()               # 다음 페이지 넘기기 클릭
                break
        return self.linkdf

    # 다음 페이지 넘기는 함수
    def isnext(self):
        try:         # 만약 다음 페이지를 넘기는 요소가 있다면
            n_btn = self.driver.find_element(By.CLASS_NAME, "next_n")
        except:      # 요소가 없으면 False 반환
            n_btn = False
        
        return n_btn # 다음페이지 정보 넘기기

    # 다음 페이지의 데이터 크롤링
    def nextpage(self, pos):
        self.waiting()

        for item in self.driver.find_elements(By.CLASS_NAME, "c_row"):
            # 해당 태그 자식 정보 중 링크를 가진 요소로부터 링크 가져오기
            li = item.find_element(By.CLASS_NAME, "c_col").find_element(By.CLASS_NAME, 
                "cell_mid").find_element(By.CLASS_NAME, "cl_top").find_element(By.TAG_NAME, "a")
            # 임시 데이터프레임 저장
            tmp = pd.DataFrame([[pos, li.get_attribute('href'), 'F']] , columns=super().getlinkcol())
            self.linkdf = pd.concat([self.linkdf, tmp], ignore_index=True)  # 데이터 저장

    # link -> data 함수
    def getdata(self):
        self.linkdf.drop_duplicates(inplace=True)   # 중복 제거
        for pos, URL in zip(self.linkdf['position'], self.linkdf['link']):  # 링크 방문하면서 데이터 조회
            self.driver.get(URL)        # 링크 방문
            self.waiting()              # 갱신 대기

            try:
                content = self.driver.find_element(By.TAG_NAME, "iframe")   # 프레임 요소
                self.driver.switch_to.frame(content)                        # 프레임 전환
                data = self.driver.find_element(By.ID, "content_job").text  # 텍스트 데이터 가져오기
            except:                     # 만약 요소가 없다면
                data = None             # 빈 데이터를 반환

            tmp = pd.DataFrame([[pos, data, 'F']], columns=super().getdatacol()) # 임시 데이터프레임
            self.datadf = pd.concat([self.datadf, tmp], ignore_index=True)   # 데이터 합치기
        return self.datadf
