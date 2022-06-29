import pandas as pd
import torch
from torch import nn
from torch.optim import Adam

from transformers import BertModel
from transformers import BertTokenizer

import numpy as np
import os


tokenizer = BertTokenizer.from_pretrained('bert-base-cased')    # bert base model 사용
labels = {  # 인덱스 설정
    'backend%20developer': 0,
    'software': 1,
    'system': 2,
    'database': 3,
    'network': 4,
    'Frontend%20Developer': 5,
    'Application': 6,
    'Service': 7,
    'Game%20Developer': 8,
    'AI%20Engineer': 9
}


class Dataset(torch.utils.data.Dataset):

    def __init__(self, df):
        self.labels = [labels[label] for label in df['category']]   # 라벨로 인덱스 설정
        self.texts = [tokenizer(text,       # 단어 토큰화
                                padding='max_length', max_length=512, truncation=True,
                                return_tensors="pt") for text in df['text']]

    # 라벨 반환 함수
    def classes(self):
        return self.labels

    # 라벨 길이 반환 함수
    def __len__(self):
        return len(self.labels)

    # Fetch a batch of labels
    def get_batch_labels(self, idx):
        return np.array(self.labels[idx])

    # Fetch a batch of inputs
    def get_batch_texts(self, idx):
        return self.texts[idx]

    # 인덱스와 데이터 가져오는 함수
    def __getitem__(self, idx):

        batch_texts = self.get_batch_texts(idx)
        batch_y = self.get_batch_labels(idx)

        return batch_texts, batch_y


class BertClassifier(nn.Module):

    def __init__(self, dropout=0.5):

        super(BertClassifier, self).__init__()  # nn.Module 상속

        self.bert = BertModel.from_pretrained('bert-base-cased')    # bert-base 모델 사용
        self.dropout = nn.Dropout(dropout)      # set dropout
        self.linear = nn.Linear(768, 10)        # 분류할 클래스가 10개
        self.relu = nn.ReLU()                   # relu 활성화함수

    def forward(self, input_id, mask):

        _, pooled_output = self.bert(input_ids=input_id, attention_mask=mask, return_dict=False)
        dropout_output = self.dropout(pooled_output)
        linear_output = self.linear(dropout_output)
        final_layer = self.relu(linear_output)

        return final_layer


class BertClassification:

    def __init__(self):
        self.model = BertClassifier()
        model_path = os.getcwd()+"/Firebase/data/bert_classifi_model.pt"
        self.checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
        self.optimizer = Adam(BertClassifier().parameters(), lr=1e-6)  # init optimizer

    def loader(self):
        self.model.load_state_dict(self.checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(self.checkpoint['optimizer_state_dict'])

    def evaluate(self, sentence):
        sample = [['database', sentence]]
        data = pd.DataFrame(sample, columns=['category', 'text'])
        test = Dataset(data)
        test_dataloader = torch.utils.data.DataLoader(test, batch_size=2)
        device = torch.device("cpu")    # 테스트시에는 cpu할 사용할 예정
        self.model.cpu()                # cpu로 조정

        with torch.no_grad():
            for test_input, _ in test_dataloader:   # 입력 데이터만 필요
                mask = test_input['attention_mask'].to(device)  # cpu
                input_id = test_input['input_ids'].squeeze(1).to(device)    # cpu

                output = self.model(input_id, mask)  # 모델 결과
                m = nn.Softmax(dim=1)                # softmax로 숫자값 추출
                # this output sample: [[idx_0, idx_1, idx_2, idx_3, idx_4,
                #                       idx_5, idx_6, idx_7, idx_8, idx_9]]
                return m(output).cpu().numpy()[0]    # 결과 출력
