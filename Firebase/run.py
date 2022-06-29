from Cluster import Cluster  # 클러스터링 모듈 불러오기
from BertClassification import BertClassification    # 학습 및 연동 모듈 불러오기
import numpy as np


def main():
    # TODO: 아래에서 API에서 받아오는 함수 필요!
    board_idx = '1'             # API로부터 얻었던 board pk 값
    pj_name = 'waitform-sample' # 파이어베이스 프로젝트 이름
    cus = Cluster(board_idx)    # 필요 데이터 넣기
    cus.connect(pj_name)        # firebase 연결
    sen, member_idx = cus.getboard()    # 게시물 값 가져오기

    b_class = BertClassification()  # 학습된 모델 불러오기
    b_class.loader()                # 모델 준비
    sample = b_class.evaluate(sen)  # 모델 결과 뽑기

    merged_sample = np.append(sample, np.array([member_idx]))
    cus.getmembers(merged_sample)   # 클러스터링을 위한 모든 데이터 가져오기(클래스 내부적으로 저장됨)

    # TODO: 아래에서 API를 호출해서 보내주는 작업 필요!
    # members = cus.cluster()   # 클러스터링 옛날 버전
    members = cus.sortby(sample, 5)    # 클러스터링 새 버전, 상위 n개 추출

    print("클러스터링 결과:", members)     # 클러스터링 결과: [192 191 183 162 198]


if __name__ == '__main__':
    main()
