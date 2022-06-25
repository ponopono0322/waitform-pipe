import crawling_wanted
import crawling_incruit

def main():
    # url = "https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=company.response_rate_order&years=-1&locations=all"
    # c_wanted = crawling_wanted.Wanted(url, True)
    # c_wanted.getlink()
    # c_wanted.getdata()

    url = "https://job.incruit.com/jobdb_list/searchjob.asp?ct=1&ty=1&cd=150"
    c_incruit = crawling_incruit.Incruit(url, False)
    c_incruit.getlink()
    c_incruit.getdata()

if __name__ == '__main__':
    main()