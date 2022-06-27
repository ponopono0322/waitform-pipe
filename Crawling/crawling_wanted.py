import time
import pandas as pd

from selenium.webdriver.common.by import By

from ChromeDriver import chromedriver

class Wanted(chromedriver):

    # 생성자
    def __init__(self, url, debug=False):
        super().__init__(debug=debug)           # chromedriver 상속
        self.URL = url                          # 접속 주소
        self.columns = {                        # 컬럼 사전 정의
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

    # 링크 데이터 크롤링 함수
    def getlink(self):      
        for c_name, p_name in self.columns.items():         # 컬럼 사전으로부터 데이터 크롤링 시도
            self.driver.get(self.URL)                       # 원티드 사이트 개발자 주소
            self.driver.implicitly_wait(time_to_wait=60)    # 사이트 갱신 대기
            try:                # 목록 창
                dr = self.driver.find_element(By.CLASS_NAME, "JobCategory_JobCategory__btn__k3EFe")
                dr.click()      # 목록창 열기
                time.sleep(1)   # 잠깐 대기
            except:
                continue

            for position in p_name:             # 사전 value 값 가져오기
                for i in self.driver.find_elements(By.TAG_NAME, "button"):  # 버튼 태그 목록 가져와서
                    if i.text == position:      # 사전 value 값과 비교
                        i.click()               # 같다면 선택하기
            # 조건 검색하기 버튼
            tg = self.driver.find_element(By.CLASS_NAME, 
                    "Button_Button__label__1Kk0v").find_element(By.XPATH, "..")
            tg.click()      # 선택된 태그로 검색하기

            time.sleep(1)
            self.scroll(c_name)     # 스크롤 함수 실행
        return self.linkdf

    # 스크롤을 통한 데이터 수집
    def scroll(self, pos):
        # 스크롤 내리기 이동 전 위치
        scroll_location = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # 현재 스크롤의 가장 아래로 내림 
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") 
            # 전체 스크롤이 늘어날 때까지 대기 
            time.sleep(2)
            # 늘어난 스크롤 높이 
            scroll_height = self.driver.execute_script("return document.body.scrollHeight") 
            # 늘어난 스크롤 위치와 이동 전 위치 같으면(더 이상 스크롤이 늘어나지 않으면) 종료 
            if scroll_location == scroll_height:
                break 
            # 같지 않으면 스크롤 위치 값을 수정하여 같아질 때까지 반복 
            else: # 스크롤 위치값을 수정
                scroll_location = self.driver.execute_script("return document.body.scrollHeight")
            break
        time.sleep(1)
        # 링크 데이터를 가진 클래스
        div = self.driver.find_elements(By.CLASS_NAME, "Card_className__u5rsb")

        for item in div:    # 데이터 순회
            link = item.find_element(By.TAG_NAME, "a").get_attribute('href')    # 링크 수집
            tmp = pd.DataFrame([[pos, link, 'F']], columns=super().getlinkcol())# 임시 데이터프레임
            self.linkdf = pd.concat([self.linkdf, tmp], ignore_index=True)      # 데이터프레임 합치기
            
    # link -> data 함수
    def getdata(self):
        self.linkdf.drop_duplicates(inplace=True)   # 중복 제거
        for pos, URL in zip(self.linkdf['position'], self.linkdf['link']):  # 링크 방문하면서 데이터 조회
            self.driver.get(URL)        # 링크 방문
            self.waiting()              # 갱신 대기
            try:                        # 요소가 있는지 검사, 있다면 텍스트 데이터 가져오기
                data = self.driver.find_element(By.CLASS_NAME, "JobContent_descriptionWrapper__SM4UD").text
            except:                     # 만약 요소가 없다면
                data = None             # 빈 데이터를 반환

            tmp = pd.DataFrame([[pos, data, 'F']], columns=super().getdatacol())     # 임시 데이터프레임
            self.datadf = pd.concat([self.datadf, tmp], ignore_index=True)  # 데이터 합치기
        return self.datadf
