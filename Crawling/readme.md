# Crawling Guide

## Crawling Columns Guide
- 아래 기준은 우리가 임의로 구성한 값입니다. 따라서 정확한 분류가 아닙니다.
- 컬럼 값은 사이트에서 가져온 데이터이므로 현재와는 다를 수 있습니다.

|Column Name|Incruit|Saramin|Programmers|Wanted|
|:---------:|:-----:|:-----:|:---------:|:----:|
|Backend |웹 프로그래머 |웹개발, 웹마스터, 풀스택, Ajax, 반응형웹, 백엔드/서버개발, 액션스크립트, ciso, cpo, 블록체인 |서버/백엔드, 웹 풀스택, 블록체인 |웹 개발자, Node.js개발자, PHP개발자, 블록체인 플랫폼 엔지니어, CTO, 루비온레일즈 개발자 |
|Software |응용프로그래머 |.NET, ABAP |응용프로그램 |소프트웨어 엔지니어, 자바 개발자, 파이썬 개발자, C/C++개발자, .NET개발자 |
|System |시스템 프로그래머 |아두이노, 그누보드, 라즈베리파이, 어셈블리, 임베디드 리눅스 |시스템 소프트웨어, 임베디드 소프트웨어, 로보틱스 미들웨어, 사물인터넷, 데브옵스 |DevOps /시스템개발자, 시스템/네트워크 개발자, 임베디드 개발자, 하드웨어 개발자 |
|DataBase |데이터베이스 |데이터 엔지니어, ABAP, 파워빌더, 모델링 |데이터 엔지니어 |데이터 엔지니어, DBA |
|Network/Security |네트워크,서버,보안 |보안컨설팅, 정보보안, 네트워크, 모의해킹, 방화벽, 와이어샤크, AIX, 미들웨어 |시스템/네트워크, 인터넷 보안 |서버 개발자, 시스템/네트워크 개발자, 보안 엔지니어 |
|Frontend |웹디자인 |퍼블리셔, 프론트엔드 |안드로이드 앱, 아이폰 앱 |프론트엔드 개발자, 웹 퍼블리셔 |
|Application |통신 모바일 |미들웨어, 안드로이드 |안드로이드 앱, 아이폰 앱 |안드로이드 개발자, IOS개발자, 크로스플랫폼 앱 개발자 |
|Service |it기술지원 |기술지원, 유지보수 |QA |개발 매니저, QA 테스트 엔지니어, 기술지원, 프로덕트 매니저, ERP 전문가, CIO |
|Game |게임 |게임개발 |모바일 게임, 게임 클라이언트, 게임서버 |VR엔지니어 |
|AI |인공지능/빅데이터 |빅데이터분석가, 데이터개발, 데이터마이닝, 시각화, 딥러닝, 머신러닝, 빅데이터 |머신러닝, 인공지능(AI) |머신러닝 엔지니어, 데이터 사이언티스트, 빅데이터 엔지니어, BI 엔지니어 |

## Directory Guide
현재 이 폴더 구조는 다음과 같습니다.
```bash
waitform-pipe
├── Crwaling                    # crawling folder
│   ├── data                    # 크롤링 데이터 폴더
│   │   ├── data.zip            # 공고문 데이터(csv) 압축 파일
│   │   └── link.zip            # 링크 데이터(csv) 압축 파일
│   │
│   ├── ChromeDriver.py         # 셀레니움 크롬드라이버 실행관련 클래스
│   ├── crawling_incruit.py     # 인크루트 크롤러
│   ├── crawling_wanted.py      # 원티드 크롤러
│   ├── crawling_linkedin.py    # 링크드인 크롤러
│   ├── crawling_programmers.py # 프로그래머스 크롤러
│   ├── crawling_saramin.py     # 사람인 크롤러
│   ├── CSVhandler.py           # csv 파일 관리
│   └── run.py                  # 시작 파일
:   :
```

## Requirements
위 파일을 실행하기 위한 필요 라이브러리입니다. 다음 명령어 실행하거나 버전을 확인하세요.
```bash
pip install -r Crawling/requirements.txt
```
- numpy==1.23.0
- pandas==1.4.3
- selenium==4.3.0
- beautifulsoup4==4.11.1
- chromedriver-autoinstaller==0.3.1

## Take a look..
csv 파일의 행은 다음과 같이 구성되어 있습니다.
- data.csv
  - `position`, `data`, `visited`
  - `position`: column name 중 하나입니다.
  - `data`    : 공고문 본문 데이터입니다.
  - `visited` : 이 데이터를 학습 데이터로 사용했는지 값('T'/'F', type=str)입니다. 
- link.csv
  - `position`,`link`, `visited`
  - `position`: column name 중 하나입니다.
  - `link`    : 링크 본문 데이터입니다.
  - `visited` : 이 데이터로 공고문 본 데이터를 크롤링 사용했는지 값('T'/'F', type=str)입니다. 

## Notice
본 가이드는 한글 본문 데이터 크롤링을 다룹니다. [부모 프로젝트](https://github.com/ALGO-LEARN/waitForm)에서 사용한 데이터(영문)와는 다릅니다.  
만약 영문 데이터(링크드인)를 크롤링하려면 다음 명령어를 통해 `crawling_linkedin.py`를 실행하거나
```bash
python Crawling/crawling_linkedin.py
```
이 [데이터](https://drive.google.com/file/d/1znx3eplfHFf8UcUX5Z-E9eDIG3cQzxQI/view?usp=sharing)를 다운받으세요.


## Crawling Example
- 다음과 같은 명령어를 통해 전체 사이트에 대한 크롤링을 수행할 수 있습니다.
  ```bash
  >>> (wait) [os-name] waitform-pipe % python Crawling/run.py
  ```
- 사이트에 대한 링크와 데이터를 파일로 저장하고 싶다면 `run.py`파일에 다음과 같은 절차를 수행하세요.
    ```python
    # 1. 먼저 CSVhandler 클래스를 불러옵니다
    from CSVhandler import CSVhandler
    cvhd = CSVhandler()

    # 2. 파일명(경로+이름+.csv)과 타입("link")을 지정합니다
    link_path = "[filename].csv"
    data_path = "[filename].csv"

    # 3. crawling() 함수에서 save_ops argument를 True로 변경합니다(기본값 False)
    crawling(cvhd, c_wanted, link_path, data_path, save_ops=True)

    # 4. 다음 경로에서 확인하세요
    waitform-pipe/Crawling/data/[filename].csv
    ```
