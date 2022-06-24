# waitform-pipe
이 레포는 [ALGO-LEARN/waitForm](https://github.com/ALGO-LEARN/waitForm)에 기반합니다.  
프로젝트 중 수행했던 작업에 대한 설명과 일부 작업 자동화를 수행하였습니다. 전체 프로세스에 대한 정보는 위의 링크를 참고해주세요.

## Directory Info
```bash
waitform-pipe
├── Crwaling        # crawling folder
│   └── *.py        # crawling code
│
├── Models          # deep-learning model folder
│   └── *.py        # crawling code
│
├── Workflow        # framework image folder
│   └── *.png       # used in readme.md
│
├── .gitignore      # gitignore
└── README.md       # readme
```

## Prerequisites
- python 3.7
- pytorch 1.9
- 기타 라이브러리는 `requirements.txt`를 참고해주세요.

## Environment Setting
아래의 설치법 중 익숙한 환경으로 구성하세요.  
1. Conda
- `requirements.yaml` 파일로 쉽게 설치하세요.
  ```bash
  conda env create -f requirements.yaml
  ```

2. pip
   ```bash
   pip install -r requirements.txt
   ```

3. Docker
   ```bash

   ```