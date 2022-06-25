import crawling_wanted
import crawling_incruit
import pandas as pd


def main():
    # wanted 사이트
    url = "https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=company.response_rate_order&years=-1&locations=all"
    c_wanted = crawling_wanted.Wanted(url, False)       # 새 객체 생성
    c_wanted.getlink()                                  # 링크 데이터 크롤링

    # incruit 사이트
    url = "https://job.incruit.com/jobdb_list/searchjob.asp?ct=1&ty=1&cd=150"
    c_incruit = crawling_incruit.Incruit(url, False)    # 새 객체 생성
    c_incruit.getlink()                                 # 랑크 데이터 크롤링

    df = pd.concat([c_incruit.getdata(), c_wanted.getdata()], ignore_index=True)
    df.to_csv("data.csv", encoding='utf-8', index=False)    # 데이터 csv 저장

    c_wanted.quit()     # 크롬 드라이버 종료
    c_incruit.quit()    # 크롬 드라이버 종료

    del c_wanted        # 소멸자 부름
    del c_incruit       # 소멸자 부름

if __name__ == '__main__':
    main()