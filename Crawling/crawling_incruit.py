import time
import pandas as pd

from selenium.webdriver.common.by import By

from ChromeDriver import chromedriver

class Incruit(chromedriver):

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
            sh.click()      # 선택된 태그로 검색하기
            
            n_btn = True
            while n_btn:
                self.nextpage(c_name)
                n_btn = self.isnext()

                if n_btn:
                    n_btn.click()
                break
            break
            time.sleep(1)

    def isnext(self):
        try:
            n_btn = self.driver.find_element(By.CLASS_NAME, "next_n")
        except:
            n_btn = False
        
        return n_btn

    def nextpage(self, pos):
        self.waiting()

        for item in self.driver.find_elements(By.CLASS_NAME, "c_row"):
            li = item.find_element(By.CLASS_NAME, "c_col").find_element(
                By.CLASS_NAME, "cell_mid").find_element(By.CLASS_NAME, "cl_top").find_element(By.TAG_NAME, "a")
            tmp = pd.DataFrame([[pos, li.get_attribute('href')]] , columns=['position', 'link'])
            self.linkdf = pd.concat([self.linkdf, tmp], ignore_index=True)
