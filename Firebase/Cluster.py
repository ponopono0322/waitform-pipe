import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import numpy as np
import os


class Cluster:

    def __init__(self, board_idx):
        self.df = None              # 모든 사용자의 데이터를 저장할 데이터프레임
        self.dblink = None          # firebase 연동 객체를 담는 변수
        self.board_idx = board_idx  # 게시물 데이터
        # firebase 내 컬럼 값
        self.column = ['c0', 'c1', 'c2', 'c3', 'c4',
                       'c5', 'c6', 'c7', 'c8', 'c9', 'id']

    # DB 연결 함수
    def connect(self, pj_name):
        # 아직 연동한 프로젝트가 없다면
        if not firebase_admin._apps:
            # 서비스 키를 사용해서 연동
            path = os.getcwd()+"/Firebase/data/serviceAccountKey.json"
            cred = credentials.Certificate(path)
            firebase_admin.initialize_app(cred, {   # 프로젝트 초기화
                'projectId': pj_name                # 프로젝트 명에 따라 적용
            })
        self.dblink = firestore.client()            # 파이어베이스 클라이언트 접속

    # 게시물 데이터 반환 함수
    def getboard(self):
        import re
        board = self.dblink.collection(u'BOARD').document(
            u"%s" % self.board_idx)                 # db에서 가져올 데이터 설정
        board_data = board.get()                    # 데이터 가져오기
        if board_data.exists:                       # 데이터가 존재한다면
            tmp = board_data.to_dict()              # 사전 타입으로 변경
            # 게시물 데이터, 게시물 쓴 사람
            return re.sub('(<([^>]+)>)', '', tmp['content']), tmp['member']['id']
        else:
            return None, None                       # 데이터가 없다면 None 반환

    # 모든 사용자 데이터 반환 함수
    def getmembers(self, class_arr):
        # 글에 대한 특징값 배열을 데이터프레임으로 변환
        usr_df = pd.DataFrame([class_arr], columns=self.column)
        if self.dblink:     # db에 데이터가 있다면
            # 사용자 정보 긁어오기
            docs = self.dblink.collection(u'MEMBER').stream()
            # 사용자 정보 데이터프레임 생성
            self.df = pd.DataFrame(columns=self.column)

            for i, doc in enumerate(docs):  # 사용자 수 만큼 반복
                # 임시 데이터프레임에 저장
                tmp = pd.DataFrame(doc.to_dict(), index=[i])
                self.df = pd.concat([self.df, tmp])  # 합치기
            # 특징값과 함께 데이터프레임 완성
            self.df = pd.concat([self.df, usr_df])
        else:               # db에 데이터가 없거나 문제가 생겼다면
            return "no connection!"

    # 가상 사용자 생성 함수
    def creator(self, n=1000):
        import torch
        from torch import nn

        c_arr = []          # 가상 사용자 데이터를 담을 배열
        for _ in range(n):  # n회 반복
            arr2 = []       # 각 사용자의 데이터를 담을 배열
            for i in range(10):  # 컬럼 수가 10개 이므로 10회만
                # 2의 i승 사이의 값으로 설정
                arr3 = np.random.randint(2 ** i, 2 ** (i + 1))
                arr2.append(arr3)   # 배열에 추가
            arr2 = np.random.permutation(arr2)  # 배열 섞기
            c_arr.append(arr2 / np.linalg.norm(arr2))   # 정규화 수행

        m = nn.Softmax(dim=1)       # softmax 클래스 가져오기
        fake_arr = m(torch.Tensor(c_arr)).numpy()   # softmax 적용
        fake_arr = np.append(fake_arr, [[i] for i in range(1, n + 1)], axis=1)

        for i, j in enumerate(fake_arr):    # 만들어진 가짜 배열을 파이어베이스에 적용
            data = self.dblink.collection(u'MEMBER')    # 사용자 테이블에 적용
            data.document(u"%d" % (i + 1)).set({u'%s' % a: b for a, b in zip(self.column, j)})

    # csv파일로부터 파이어베이스 가짜 데이터 적용
    def creatorbycsv(self, df):
        for i, j in enumerate(df.to_dict('records')):   # 데이터프레임 사전 타입 전환
            data = self.dblink.collection(u"MEMBER")    # 사용자 테이블 지정
            data.document(u"%d" % (i + 1)).set(j)       # 데이터 저장

    # 500개의 가짜 데이터 생성
    def checker(self, csv_name="conv.csv"):
        df = pd.read_csv(csv_name, encoding='utf-8')  # 파일 읽어오기
        cov_df = pd.DataFrame(columns=['c0', 'c1', 'c2', 'c3', 'c4', 'c5',
                                       'c6', 'c7', 'c8', 'c9', 'category'])
        for i in df.category.unique():                    # 10개의 컬럼 값
            df2 = df[df['category'] == i].sample(n=50)    # 각 컬럼당 무작위 50개를 뽑아서
            cov_df = pd.concat([cov_df, df2])             # 새 데이터 프레임에 합치기
        cov_df.reset_index(drop=True, inplace=True)       # 인덱스 초기화
        cov_df['id'] = [i for i in range(1, 501)]         # id 값 설정
        cov_df.drop(['category'], axis=1, inplace=True)   # 컬럼 정보 삭제
        self.creatorbycsv(cov_df)                         # 데이터베이스에 저장

    # FIXME: 반복문 때문에 일부 사용자 없다면 오류
    def clear(self, n=1000):    # 모든 사용자 제거 함수
        for i in range(n):
            self.dblink.collection(u'MEMBER').document(u"%d" % (i + 1)).delete()

    # 클러스터링 함수
    def cluster(self, k=10, max_return=5):    # 클러스터링
        from sklearn.cluster import KMeans

        model = KMeans(n_clusters=k, random_state=10)   # KMeans 클래스 사용
        arr = self.df.drop(['id'], axis=1).to_numpy()   # id 컬럼은 사용하지 않으므로 제거
        model.fit(arr)                                  # 학습
        self.df['cluster'] = model.fit_predict(arr)     # 예측된 결과 컬럼 추가

        num = self.df.iloc[-1]['cluster']               # 클러스터링 된 인덱스 번호
        cdata = np.array(self.df.iloc[-1][:10])         # 입력 들어온 값의 데이터
        same_data = self.df[self.df['cluster'] == num]  # 같은 클러스터 데이터프레임

        result = np.array([])                           # 추천 유저 리스트
        for i in same_data.index:                       # 같은 클러스터 반복
            s = np.array(same_data.loc[i])[:10]         # 각 row 넘파이 변환
            dist = np.linalg.norm(cdata-s)              # 거리 공식
            result = np.append(result, [dist])          # 거리 추가
        max_return += 1     # 인덱스 슬라이딩 때문에 추가
        # 가장 근접한 데이터 저장
        members = np.argpartition(result, (1, max_return))[1:max_return]
        return [int(i) for i in members]                # 인덱스 출력

    # 가장 근접한 결과를 출력하는 함수
    def sortby(self, m_result, n):
        sort_arr = [self.column[i] for i in np.argpartition(
            -m_result, (1, len(m_result)-1))]
        return self.df.sort_values(
            by=sort_arr, axis=0, ascending=False)['id'][:n].to_numpy()

    # 데이터 갱신 함수
    def update(self, member_idx, class_arr):
        # 데이터베이스에서 해당 사용자의 정보를 저장
        member = self.dblink.collection(u'MEMBER').document(u"%s" % member_idx)
        member_data = member.get()  # 데이터 기져오기
        if member_data.exists:      # 데이터가 존재하는 경우만
            tmp = member_data.to_dict()     # 사전 타입으로 변경
            legacy_data = np.array([tmp[c] for c in self.column])   # 기존데이터
            update_data = (legacy_data + class_arr) / 2.0           # 갱신데이터
            # 갱신 데이터 적용
            member.update({u'%s' % i: j for i, j in zip(self.column, update_data)})

        else:   # 사용자를 찾지 못한 경우
            print("Failed: member data update")  # 갱신 오류임을 알림

    # 실제 사용한 학습 데이터로 softmax값을 뽑는 함수
    def csvdbmaker(self, model_path, data_path, csv_name="conv.csv"):
        from BertClassification import BertClassification
        b_class = BertClassification(model_path)
        b_class.loader()    # 테스트하는 것과 같게
        # 실제 사용한 데이터셋의 데이터를 불러와서 중복값, 결측값 제거
        df = pd.read_csv(data_path).dropna().drop_duplicates(ignore_index=True)
        ans_arr = []        # softmax 결과값을 저장하기 위한 함수

        for i, j in zip(df['category'], df['text']):
            sample = b_class.evaluate([[i, j]])                 # 모델로 결과 뽑기
            ans_arr.append(np.append(sample, np.array([i])))    # 데이터 추가
        # 데이터 프레임으로 전환
        df2 = pd.DataFrame(ans_arr, columns=['c0', 'c1', 'c2', 'c3', 'c4',
                                             'c5', 'c6', 'c7', 'c8', 'c9', 'category'])
        df2.to_csv(csv_name, index=False, encoding='utf-8')     # 데이터 저장
