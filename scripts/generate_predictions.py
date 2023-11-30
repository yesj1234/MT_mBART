import argparse
import torch
from tqdm import tqdm
import logging 
import sys
import re 
from time import time 
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from datasets import load_dataset 
import evaluate
import math
import numpy as np

class Translator:
    def __init__(self, args):
        self.args = args
        self.src_lang = args.src_lang.split("_")[0]
        self.tgt_lang = args.tgt_lang.split("_")[0]
        self.predictions = []
        self.references = []
        self.bleu = []
        self.metric = evaluate.load("sacrebleu")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = MBartForConditionalGeneration.from_pretrained(self.args.model_repo).to(self.device)
        self.tokenizer = MBart50TokenizerFast.from_pretrained(self.args.model_repo)
        self.SACREBLEU_TOKENIZE = {
            "ko_KR": "ko-mecab",
            "ja_XX": "ja-mecab",
            "en_XX": "char",
            "zh_CN": "zh"
        }
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
            handlers=[logging.StreamHandler(sys.stdout)],
        )

    def _load_data(self):
        return load_dataset("json", data_files=self.args.data, field="translation")["train"]

    def _generate_predictions(self, batch):
        src_text = batch[self.src_lang]
        tgt_text = batch[self.tgt_lang]
        model_inputs = self.tokenizer(src_text, max_length=200, truncation=True, padding=True, return_tensors="pt").to(self.device)
        with torch.no_grad():
            generated_tokens = self.model.generate(**model_inputs).to(self.device)
        prediction = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        self.predictions.extend(prediction)
        self.references.extend(tgt_text)

    def _my_log(self, num):
        if num == 0.0:
            return -9999999999
        return math.log(num)

    def compute_bleu(self, preds, refs):
        result = self.metric.compute(predictions=preds, references=refs, tokenize=self.SACREBLEU_TOKENIZE[self.args.tgt_lang])
        bp = result["bp"]
        precisions = result["precisions"]
        bleu_score = bp * math.exp(sum([self._my_log(p) for p in precisions[:3]]) / 3)
        result = {"bleu": bleu_score}
        prediction_lens = [np.count_nonzero(pred != self.tokenizer.pad_token_id) for pred in preds]
        result["gen_len"] = np.mean(prediction_lens)
        result = {k: round(v, 4) for k, v in result.items()}
        return result

    def run_translation(self):
        start_time = time()

        raw_dataset = self._load_data()

        raw_dataset.map(lambda x: self._generate_predictions(x), batched=True, batch_size=30)
        self.predictions = list(map(lambda x: "".join(list(x.strip())).lower(), self.predictions))
        self.references = list(map(lambda x: "".join(list(x.strip())).lower(), self.references))
        self.references = list(map(lambda x: [x], self.references))

        for pred, ref in zip(self.predictions, self.references):
            bleu_score = self.compute_bleu(preds=[pred], refs=[ref])
            self.bleu.append(bleu_score['bleu'])
        
        with open(f"{self.args.file_name}.txt", "w+", encoding="utf-8") as f:
            for pred, ref, bleu in zip(self.predictions, self.references, self.bleu):                
                f.write(f"{pred} :: {ref[0]} :: {bleu}\n")

        try:
            result = self.compute_bleu(preds=self.predictions, refs=self.references)
            self.logger.info(f"""
                        ***** eval metrics *****
                          eval_samples: {len(self.predictions)}
                          eval_result : {result}
                          eval_runtime: {time() - start_time} 
                        """)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_repo", help="fine-tuned model dir. relative dir path or repo_id from huggingface")
    parser.add_argument("--data", help="path to test data in json format")
    parser.add_argument("--src_lang", help="ko_KR ja_XX zh_CN en_XX")
    parser.add_argument("--tgt_lang", help="ko_KR ja_XX zh_CN en_XX")
    parser.add_argument("--file_name", help="file name to save generated predictions")
    args = parser.parse_args()

    translator = Translator(args)
    translator.run_translation()
