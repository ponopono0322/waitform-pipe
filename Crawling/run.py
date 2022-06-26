import crawling_wanted
import crawling_incruit
import pandas as pd


def main():
    link_path = "./data/link.csv"
    data_path = "./data/data.csv"
    # wanted 사이트
    url = "https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=company.response_rate_order&years=-1&locations=all"
    c_wanted = crawling_wanted.Wanted(url, True)       # 새 객체 생성
    wl_tmp = c_wanted.getlink()                        # 링크 데이터 크롤링
    w_tmp = c_wanted.getdata()
    c_wanted.close()

    # incruit 사이트
    url = "https://job.incruit.com/jobdb_list/searchjob.asp?ct=1&ty=1&cd=150"
    c_incruit = crawling_incruit.Incruit(url, True)    # 새 객체 생성
    il_tmp = c_incruit.getlink()                       # 랑크 데이터 크롤링
    i_tmp = c_incruit.getdata()
    c_incruit.close()

    df = pd.concat([wl_tmp, il_tmp], ignore_index=True)
    c_incruit.mergecsv(link_path, df)

    df = pd.concat([w_tmp, i_tmp], ignore_index=True)
    c_incruit.mergecsv(data_path, df)

    c_wanted.quit()     # 크롬 드라이버 종료
    c_incruit.quit()    # 크롬 드라이버 종료

    del c_wanted        # 소멸자 호출
    del c_incruit       # 소멸자 호출

    return 0

if __name__ == '__main__':
    main()