import crawling_wanted

def main():
    url = "https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=company.response_rate_order&years=-1&locations=all"
    c_wanted = crawling_wanted.Wanted(url, True)
    c_wanted.getlink()
    c_wanted.getdata()

if __name__ == '__main__':
    main()