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

## Crawling Example
- 다음 명령어를 통해 전체 사이트에 대한 크롤링을 수행할 수 있습니다.
  ```bash
  # 아래와 같이 waitform-pipe의 최상위 폴더에서 Crawling 폴더로 이동하세요
  # (wait) [os-name] Crawling %
  >>> (wait) [os-name] Crawling % python run.py
  ```
- 사이트에 대한 링크나 데이터를 독립적인 파일로 저장하고 싶다면 `run.py`파일에 다음과 같은 절차를 수행하세요.
  - 링크 데이터를 저장하고 싶은 경우  
    ```python
    # 1. 먼저 getlink() 함수를 실행합니다
    c_wanted.getlink()

    # 2. 파일명(이름+.csv)과 타입("link")을 지정합니다.
    file_name = "link_filename.csv"
    file_type = "link"

    # 3. exporttocsv() 함수를 실행시킵니다.
    c_wanted.exporttocsv(path=file_name, type=file_type)
    ```
  - 공고문 데이터를 저장하고 싶은 경우
    ```python
    # 1. 먼저 getdata() 함수를 실행합니다
    c_wanted.getdata()

    # 2. 파일명(이름+.csv)과 타입("data")을 지정합니다.
    file_name = "data_filename.csv"
    file_type = "data"

    # 3. exporttocsv() 함수를 실행시킵니다.
    c_wanted.exporttocsv(path=file_name, type=file_type)
    ```