import os 
import argparse 
import evaluate 
import math 
from tqdm import tqdm
import traceback
from datasets import load_dataset
import time 

SACREBLEU_TOKENIZE = {
    "ko_KR": "ko-mecab",
    "ja_XX": "ja-mecab",
    "en_XX": "char",
    "zh_CN": "zh"
}
class Calculator:
    def __init__(self, args):
        self.metric = evaluate.load("sacrebleu")       
        self.tgt_lang = args.tgt_lang

    def _my_log(self, num):
        if num == 0.0:
            return -9999999999
        return math.log(num)

    def _batch_compute(self, batch):
        pred, ref = batch["pairs"].split(" :: ")
        result = self.metric.compute(predictions = [pred], references = [[ref]], tokenize = SACREBLEU_TOKENIZE[self.tgt_lang])
        bleu_score = result["bp"] * math.exp(sum([self._my_log(p) for p in result["precisions"][:3]]) / 3)
        batch["score"] = bleu_score
        return batch 
           
    def translate(self, ds):
        return ds.map(self._batch_compute)
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prediction_file", help="file to use for generating each metric score")
    parser.add_argument("--tgt_lang", help="ko_KR, ja_XX, zh_CN, en_XX")
    args = parser.parse_args()
    
    calculator = Calculator(args)
    ds = load_dataset("csv", data_files = args.prediction_file)
    ds = ds["train"]
    
    shard_size = 20 
    iterable_ds = ds.shard(num_shards = shard_size, index = 0)
    for i in range(shard_size):
        iterable_ds = ds.shard(num_shards = shard_size,index = i)
        new_ds = calculator.translate(iterable_ds)
        with open(f"test_{i}th.txt", mode = "w", encoding = "utf-8") as f:
            for row in new_ds:
                f.write(f"{row}\n")
    
