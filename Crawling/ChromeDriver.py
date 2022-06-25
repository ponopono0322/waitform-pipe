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
        self.linkdf.drop_duplicates(inplace=True)   # 중복 제거
        for pos, URL in zip(self.linkdf['position'], self.linkdf['link']):  # 링크 방문하면서 데이터 조회
            if URL.find('wanted.co.kr') > 0:        # wanted 사이트인 경우
                data = self.wantedata(URL)          # 텍스트 데이터
            elif URL.find('incruit.com') > 0:       # incruit 사이트인 경우
                data = self.incruitdata(URL)        # 텍스트 데이터

            tmp = pd.DataFrame([[pos, data]], columns=['position', 'data'])     # 임시 데이터프레임
            self.datadf = pd.concat([self.datadf, tmp], ignore_index=True)      # 데이터 합치기

    # wanted 사이트 공고문 데이터
    def wantedata(self, URL):   
        self.driver.get(URL)        # 링크 방문
        self.waiting()              # 갱신 대기
        try:                        # 요소가 있는지 검사, 있다면 텍스트 데이터 가져오기
            data = self.driver.find_element(By.CLASS_NAME, "JobContent_descriptionWrapper__SM4UD").text
        except:                     # 만약 요소가 없다면
            data = None             # 빈 데이터를 반환
        return data                 # 데이터 반환

    # incruit 사이트 공고문 데이터
    def incruitdata(self, URL):
        self.driver.get(URL)        # 링크 방문
        self.waiting()              # 갱신 대기
        try:
            content = self.driver.find_element(By.TAG_NAME, "iframe")   # 프레임 요소
            self.driver.switch_to.frame(content)                        # 프레임 전환
            data = self.driver.find_element(By.ID, "content_job").text  # 텍스트 데이터 가져오기
        except:                     # 만약 요소가 없다면
            data = None             # 빈 데이터를 반환
        return data                 # 데이터 반환

    # 페이지 갱신 대기
    def waiting(self, time=60):
        self.driver.implicitly_wait(time_to_wait=time)

    # 크롬 드라이버 닫는 함수
    def close(self):
        self.driver.close()

    # 크롬 드라이버 종료 함수
    def quit(self):
        self.driver.quit()