# This code is based on
# https://gist.github.com/marcellusruben
# which from
# https://towardsdatascience.com/text-classification-with-bert-in-pytorch-887965e5820f

import numpy as np
import os
import torch
from torch import nn
from torch.optim import Adam
from tqdm import tqdm
import pandas as pd

from transformers import BertModel
from transformers import BertTokenizer


def getdf(path):
    return pd.read_csv(path).dropna().drop_duplicates(ignore_index=True)

def getlabel(path):
    df = getdf(path)
    return {j:i for i, j in enumerate(df.category.unique())}

path = os.getcwd() + '/Models/data/code_data.csv'   # 데이터셋 경로 
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')  # 토크나이저 가져오기
labels = getlabel(path)     # 데이터셋 columns 가져오기

class Dataset(torch.utils.data.Dataset):

    def __init__(self, df):
        self.labels = [labels[label] for label in df['category']]   # 라벨 설정
        self.texts = [tokenizer(text, padding='max_length', max_length = 512,   # 텍스트 설정
                                truncation=True, return_tensors="pt") for text in df['text']]
    # 라벨값 반환 함수
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

    # 아이템 반환 함수
    def __getitem__(self, idx):
        batch_texts = self.get_batch_texts(idx)     # 해당 인덱스 데이터의 값
        batch_y = self.get_batch_labels(idx)        # 해당 인덱스 데이터의 라벨

        return batch_texts, batch_y


class BertClassifier(nn.Module):

    def __init__(self, dropout=0.5):

        super(BertClassifier, self).__init__()

        self.bert =  BertModel.from_pretrained('bert-base-cased')   # bert-base-cased 모델
        self.dropout = nn.Dropout(dropout)      # 드롭아웃 0.5
        self.linear = nn.Linear(768, 10)        # 10개의 클래스를 사용하기 때문
        self.relu = nn.ReLU()                   # Relu 활성화함수

    def forward(self, input_id, mask):

        _, pooled_output = self.bert(input_ids=input_id, attention_mask=mask, return_dict=False)
        dropout_output = self.dropout(pooled_output)
        linear_output = self.linear(dropout_output)
        final_layer = self.relu(linear_output)

        return final_layer

def train(model, train_data, val_data, learning_rate, start_epoch, epochs, PATH):
    
    train, val = Dataset(train_data), Dataset(val_data)      # 커스텀 데이터셋 호출

    train_dataloader = torch.utils.data.DataLoader(          # 학습 데이터셋
        train, batch_size=2, shuffle=True)
    val_dataloader = torch.utils.data.DataLoader(            # 검증 데이터셋
        val, batch_size=2)

    use_cuda = torch.cuda.is_available()                     # GPU 사용이 가능한지
    device = torch.device("cuda" if use_cuda else "cpu")     # 사용가능하면 GPU 사용

    criterion = nn.CrossEntropyLoss()                        # 크로스엔트로피 사용
    optimizer = Adam(model.parameters(), lr= learning_rate)  # Adam 옵티마이저 적용

    if use_cuda:        # GPU 사용 가능하면
        model = model.cuda()    # 쿠다 적용
        criterion = criterion.cuda()    # 엔트로피도 쿠다 적용

    for epoch_num in range(start_epoch, epochs):    # 이전 학습한 것이 있다면 그 위치부터
        total_acc_train = 0         # 학습 데이터 정확도
        total_loss_train = 0        # 학습 데이터 손실

        for train_input, train_label in tqdm(train_dataloader):
            
            train_label = train_label.to(device)
            mask = train_input['attention_mask'].to(device)
            input_id = train_input['input_ids'].squeeze(1).to(device)

            output = model(input_id, mask)
            
            batch_loss = criterion(output, train_label)
            total_loss_train += batch_loss.item()
            
            acc = (output.argmax(dim=1) == train_label).sum().item()
            total_acc_train += acc

            model.zero_grad()
            batch_loss.backward()
            optimizer.step()
        
        total_acc_val = 0
        total_loss_val = 0

        with torch.no_grad():

            for val_input, val_label in val_dataloader:

                val_label = val_label.to(device)
                mask = val_input['attention_mask'].to(device)
                input_id = val_input['input_ids'].squeeze(1).to(device)

                output = model(input_id, mask)

                batch_loss = criterion(output, val_label)
                total_loss_val += batch_loss.item()
                
                acc = (output.argmax(dim=1) == val_label).sum().item()
                total_acc_val += acc
        
        print(
            f'Epochs: {epoch_num + 1} | Train Loss: {total_loss_train / len(train_data): .3f} \
            | Train Accuracy: {total_acc_train / len(train_data): .3f} \
            | Val Loss: {total_loss_val / len(val_data): .3f} \
            | Val Accuracy: {total_acc_val / len(val_data): .3f}')

        if (epoch_num+1) % 5 == 0:
            torch.save({
                'epoch': epoch_num,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
            }, PATH)

def evaluate(model, test_data):

    test = Dataset(test_data)

    test_dataloader = torch.utils.data.DataLoader(test, batch_size=2)

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    if use_cuda:
        model = model.cuda()

    total_acc_test = 0
    with torch.no_grad():

        for test_input, test_label in test_dataloader:

            test_label = test_label.to(device)
            mask = test_input['attention_mask'].to(device)
            input_id = test_input['input_ids'].squeeze(1).to(device)

            output = model(input_id, mask)
            m = nn.Softmax(dim=1)
            print("output:", m(output).cpu().numpy())
            acc = (output.argmax(dim=1) == test_label).sum().item()
            total_acc_test += acc
    
    print(f'Test Accuracy: {total_acc_test / len(test_data): .3f}')