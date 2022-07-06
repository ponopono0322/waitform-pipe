import os
import argparse
import pandas as pd
from ModelController import ModelControl

def main():
    path = os.getcwd() + "/Models/data/code_data.csv"
    model_path = os.getcwd() + "/Models/data/bert_classifi_model.pt"
    mc = ModelControl(path)

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

    parser = argparse.ArgumentParser(description="Model run type settings")
    parser.add_argument('--mode', choices=['train', 'eval', 'test'], type=str, required=True)
    parser.add_argument('--epoch', type=int, required=False, default=20, help="default: 20")
    parser.add_argument('--class_type', choices=range(10), type=int, required=False, help=str(class_arr))
    parser.add_argument('--sentence', type=str, required=False)

    args = parser.parse_args()

    if args.mode == 'train':
        mc.trianer(args.epoch, model_path)
    elif args.mode == 'eval':
        mc.evaluater(model_path)
    else:
        print("test mode")
        if type(args.class_type) is int and type(args.sentence) is str:
            class_name = class_arr[args.class_type]
            test_df = pd.DataFrame([[args.sentence, class_name]], columns=['text', 'category'])
            mc.eval_test(test_df, model_path)
        else:
            print("Please check arguments class_type and sentence")

if __name__ == "__main__":
    main()