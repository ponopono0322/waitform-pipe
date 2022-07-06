# Models
우리 프로젝트에서 사용했던 Classification 학습 모델입니다.

## Directory Info
```bash
waitform-pipe
├── Models
│   ├── data                # 데이터셋 폴더(이 폴더는 업로드되지 않습니다)
│   │   ├── data
│   │   └── code_data.csv   # 링크드인 크롤링 데이터(영문)
│   ├── BertTextClassification.py   # BERT를 사용한 분류 모델
│   └── functions.py        # 데이터처리, 학습, 검증, 테스트를 돕는 클래스
:   :
```

## Spec
- Ubuntu 20.04
- Nvidia GTX 1080ti (CUDA 10.2)
- 32GB DRAM
_OR Google Colab GPU mode_

## Train
모델을 처음부터 학습할 경우 `[int]` 대신에 epoch 수를 입력하세요  
```bash
python Models/run.py --mode "train" --epoch [int]
```

## Evaluate
데이터셋의 평가를 진행할 경우는 아래와 같이 진행하세요
```bash
python Models/run.py --mode "eval"
```

## Evaluate your data
자체 데이터로 결과를 얻고자 하는 경우는 `class_type`에 0~9 사이의 숫자를, `senetence`는 문장을 넣으세요.  
`class_type`에 대한 정보는 아래를 참고하세요.  

```bash
python Models/run.py --mode --class_type [int] --sentence [str]
```

```bash
class_arr = {
    0: 'backend%20developer',
    1: 'software',
    2: 'system', 
    3: 'database', 
    4: 'network', 
    5: 'Frontend%20Developer', 
    6: 'Application', 
    7: 'Service', 
    8: 'Game%20Developer', 
    9: 'AI%20Engineer'
}
```

혹은 `-h` 옵션으로 확인할 수 있습니다.
```bash
python Models/run.py -h
```

