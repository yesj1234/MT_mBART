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
import os 
import argparse 
import evaluate 
import math 
from tqdm import tqdm
import traceback
from datasets import load_dataset
import time 
import sacrebleu 

class Calculator:
    def __init__(self, args):
        self.trg_lang = args.trg_lang
        self.metric = sacrebleu.BLEU(trg_lang=self.trg_lang, max_ngram_order = 3, effective_order=True)       


    def _my_log(self, num):
        if num == 0.0:
            return -9999999999
        return math.log(num)

    def _batch_compute(self, batch):
        preds = list(map(lambda x: x.split(" :: ")[0], batch["pairs"]))
        refs = list(map(lambda x: x.split(" :: ")[1], batch["pairs"]))
        scores = []
        for pred, ref in zip(preds, refs):
          result = self.metric.sentence_score(hypothesis= pred, references=[ref]) 
          scores.append(result.score)
        batch["score"] = scores
        return batch 
           
    def calculate(self, ds):
        return ds.map(self._batch_compute, batched=True, batch_size = 100)
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prediction_file", help="file to use for generating each metric score")
    parser.add_argument("--trg_lang", help="ko, ja, zh, en")
    args = parser.parse_args()
    calculator = Calculator(args)
    ds = load_dataset("csv", data_files = args.prediction_file)
    ds = ds["train"]
    new_ds = calculator.calculate(ds)
    with open(f"{args.prediction_file}_with_score.txt", mode = "w", encoding = "utf-8") as f:
        for row in new_ds:
            f.write(f"{row}\n")
    # shard_size = 20 
    # iterable_ds = ds.shard(num_shards = shard_size, index = 0)
    # for i in range(shard_size):
    #     iterable_ds = ds.shard(num_shards = shard_size,index = i)
    #     new_ds = calculator.translate(iterable_ds)
    #     with open(f"test_{i}th.txt", mode = "w", encoding = "utf-8") as f:
    #         for row in new_ds:
    #             f.write(f"{row}\n")
    
