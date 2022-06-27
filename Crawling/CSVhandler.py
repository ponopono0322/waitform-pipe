import pandas as pd
import os
import zipfile
os.chdir('./data')

class CSVhandler:
    def __init__(self):
        pass

    # df -> csv 함수
    def exporttocsv(self, path, type='data'):
        if type == 'link':                                  # 링크 데이터 csv 저장
            self.linkdf.to_csv(path, index=False, encoding='utf-8')
        else:                                               # 공고문 데이터 csv 저장
            self.datadf.to_csv(path, index=False, encoding='utf-8')
    
    # 파일 검사
    def filecheck(self, path):
        if os.path.exists(path):
            return True
        else:
            return False

    # 새 데이터만 크롤링 힐 때
    def searchnewdata(self, path, before_df, type='data'):
        self.csvextract(path)

        if self.filecheck(path):        # 경로에 기존 파일이 있다면
            new_df = pd.concat([pd.read_csv(path), before_df], ignore_index=True)
            return self.newdata(new_df, type)
        else:
            return before_df            # 기존 데이터가 없다면 그대로 

    # 기존 데이터와 합치는 작업
    def mergecsv(self, path, before_df, type='data'):
        if type == 'link':              # 링크 데이터였을 경우만
            before_df['visited'] = 'T'  # 모든 데이터를 방문했으므로 방문값을 True로 바꿈

        if self.filecheck(path):        # 경로에 기존 파일이 있다면
            new_df = pd.concat([pd.read_csv(path), before_df], ignore_index=True)
            new_df.to_csv(path, index=False, encoding='utf-8')      # 데이터를 합친 후 저장
        else:                           # 기존 파일이 없다면
            before_df.to_csv(path, index=False, encoding='utf-8')   # 새 파일 만들기

        self.csvcompress(path)          # csv 데이터 압축
        self.csvremove(path)            # csv 데이터 삭제

    # 데이터 압축
    def csvcompress(self, path):
        zip_path = path[:-3]+"zip"      # zip 파일 경로
        
        if self.filecheck(path):        # csv 파일이 존재하는지 검사
            csv_zip = zipfile.ZipFile(zip_path, 'w')    # 압축후 파일 이름
            csv_zip.write(path, compress_type=zipfile.ZIP_DEFLATED) # 압축할 파일 이름
            csv_zip.close()             # 파일 닫기

    # 데이터 압축해제
    def csvextract(self, path):
        zip_path = path[:-3]+'zip'      # zip 파일 경로

        if self.filecheck(zip_path):    # zip 파일이 존재하는지 검사
            with zipfile.ZipFile(zip_path, 'r') as csv_zip: # 파일 열기
                csv_zip.extractall()    # 압축 해제
    
    # 데이터 삭제
    def csvremove(self, path):
        os.remove(path)                 # 파일 삭제

    # 새로운 데이터 추출
    def newdata(self, input_df, type):
        # 중복 제거 후
        conv_df = input_df.drop_duplicates(['position',type], keep='first', ignore_index=True)
        new_df = conv_df[conv_df['visited'] == 'F'] # 아직 검사하지 않은 데이터 추출

        if len(new_df) > 0:     # 새 데이터가 1개라도 있다면
            return new_df       # 새 데이터 목록 반환
        else:                   # 없다면 빈 배열 반환
            return pd.DataFrame(columns=['position', type, 'visited'])
