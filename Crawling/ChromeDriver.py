from abc import ABC
import pandas as pd
import chromedriver_autoinstaller
import os
import zipfile

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
        self.csvextract(path)

        if os.path.exists(path):   # 경로에 기존 파일이 있다면
            new_df = pd.concat([pd.read_csv(path), before_df], ignore_index=True)
            new_df.to_csv(path, index=False, encoding='utf-8')      # 데이터를 합친 후 저장
        else:                      # 기존 파일이 없다면
            before_df.to_csv(path, index=False, encoding='utf-8')   # 새 파일 만들기

        self.csvcompress(path)      # csv 데이터 압축
        self.csvremove(path)        # csv 데이터 삭제

    # 데이터 압축
    def csvcompress(self, path):
        zip_path = path[:-3]+"zip"  # zip 파일 경로
        
        if os.path.exists(path):    # csv 파일이 존재하는지 검사
            os.chdir(os.getcwd()+'/data/')  # os 경로 변경
            csv_zip = zipfile.ZipFile(zip_path[7:], 'w')    # 압축된 파일 이름
            csv_zip.write(path[7:], compress_type=zipfile.ZIP_DEFLATED) # 압축할 파일 이름
            csv_zip.close()         # 파일 닫기
            os.chdir('../')         # os 경로 복구

    # 데이터 압축해제
    def csvextract(self, path):
        zip_path = path[:-3]+'zip'      # zip 파일 경로

        if os.path.exists(zip_path):    # zip 파일이 존재하는지 검사
            with zipfile.ZipFile(os.getcwd()+zip_path[1:], 'r') as csv_zip: # 파일 열기
                csv_zip.extractall(os.getcwd()+'/data')     # 압축 해제
    
    # 데이터 삭제
    def csvremove(self, path):
        os.remove(path)     # 파일 삭제

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