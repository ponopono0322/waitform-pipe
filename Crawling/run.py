from crawling_wanted import Wanted
from crawling_incruit import Incruit
from CSVhandler import CSVhandler


def main():
    link_path = "link.csv"
    data_path = "data.csv"
    cvhd = CSVhandler()

    # wanted 사이트
    url = "https://www.wanted.co.kr/wdlist/518?country=kr&\
        job_sort=company.response_rate_order&years=-1&locations=all"
    c_wanted = Wanted(url, False)        # 새 객체 생성
    crawling(cvhd, c_wanted, link_path, data_path)

    # incruit 사이트
    url = "https://job.incruit.com/jobdb_list/searchjob.asp?ct=1&ty=1&cd=150"
    c_incruit = Incruit(url, False)     # 새 객체 생성
    crawling(cvhd, c_incruit, link_path, data_path)

    del c_wanted        # 소멸자 호출
    del c_incruit       # 소멸자 호출

    return 0


def crawling(cvhd, c_class, link_path, data_path, save_ops=False):
    cl_tmp = c_class.getlink()                         # 링크 데이터 크롤링
    if save_ops:                                       # 별도 저장 옵션을 사용한 경우
        cvhd.exporttocsv(link_path, cl_tmp, 'link')
    cl_new = cvhd.searchnewdata(link_path, cl_tmp, 'link')  # 새 데이터 찾기
    c_class.datacheck(cl_new, type='link')             # 새 데이터 적용
    c_tmp = c_class.getdata()                          # 공고문 데이터

    if save_ops:                                       # 별도 저장 옵션을 사용한 경우
        cvhd.exporttocsv(data_path, c_tmp, 'link')
    c_new = cvhd.searchnewdata(data_path, c_tmp, 'data')

    cvhd.mergecsv(link_path, cl_new, 'link')
    cvhd.mergecsv(data_path, c_new, 'data')

    c_class.close()
    c_class.quit()     # 크롬 드라이버 종료


if __name__ == '__main__':
    main()
