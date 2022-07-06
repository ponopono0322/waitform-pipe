import numpy as np
import os
import torch

from BertTextClassification import BertClassifier, train, evaluate, getdf

class ModelControl:

    def __init__(self, path):
        self.df = getdf(path)
        self.model = None
        self.df_train = None
        self.df_val = None
        self.df_test = None

    def getdataset(self):
        np.random.seed(112)
        self.df_train, self.df_val, self.df_test = np.split(
            self.df.sample(frac=1, random_state=42),
            [int(.8*len(self.df)), int(.9*len(self.df))])

        return self.df_train, self.df_val, self.df_test

    def getmodel(self):
        self.model = BertClassifier()

    def trianer(self, EPOCHS, model_path):
        start_epoch = 0
        LR = 1e-6
        self.getmodel()
        self.getdataset()

        if os.path.exists(model_path):
            checkpoint = torch.load(model_path)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            start_epoch = checkpoint['epoch']
            EPOCHS += start_epoch

        train(self.model, self.df_train, self.df_val, LR, start_epoch, EPOCHS)

    def evaluater(self, model_path):
        self.getmodel()
        if os.path.exists(model_path):
            checkpoint = torch.load(model_path)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.model.eval()
        else:
            return f"Couldn't find model {model_path}"

        evaluate(self.model, self.df_test)

    def eval_test(self, model_path, df_test):
        self.getmodel()
        if os.path.exists(model_path):
            checkpoint = torch.load(model_path)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.model.eval()
        else:
            return f"Couldn't find model {model_path}"
        
        evaluate(self.model, df_test)