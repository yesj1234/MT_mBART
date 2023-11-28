import argparse
import torch
from tqdm import tqdm
import logging 
import sys
import re 
from time import time 
from transformers import (
    MBartForConditionalGeneration, 
    MBart50TokenizerFast,
)
from datasets import load_dataset 
import evaluate
import math
import numpy as np
logger = logging.getLogger(__name__)
 # Setup logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger.setLevel(logging.DEBUG)

SACREBLEU_TOKENIZE = {
    "ko_KR": "ko-mecab",
    "ja_XX": "ja-mecab",
    "en_XX": "13a",
    "zh_CN": "zh"
}



def main(args):
    start_time = time()

    raw_dataset = load_dataset("json", data_files = args.data, field="translation")["train"]
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    model = MBartForConditionalGeneration.from_pretrained(args.model_repo).to(device)
    tokenizer = MBart50TokenizerFast.from_pretrained(args.model_repo)
    src_lang = args.src_lang.split("_")[0]
    tgt_lang = args.tgt_lang.split("_")[0]
    metric = evaluate.load("sacrebleu")
    
    references = []
    predictions = []
    def generate_predictions(batch):
        src_text = batch[src_lang]
        model_inputs = tokenizer(src_text, max_length = 200, truncation=True, padding=True,return_tensors="pt").to(device)
        with torch.no_grad():
            generated_tokens = model.generate(**model_inputs).to(device)
        prediction = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        predictions.append(prediction)
        references.append(src_text)
        
    
    def post_processing(batch):
        prediction = batch["prediction"].strip()
        prediction = "".join(list(prediction)).lower()
        reference = batch[tgt_lang].strip()
        reference = "".join(list(reference)).lower()
        batch["prediction"] = prediction
        batch["reference"] = reference
        return batch        
    
    def compute_bleu(preds, refs):  
        result = metric.compute(predictions=preds, references=refs, tokenize=SACREBLEU_TOKENIZE[args.tgt_lang])
        bp = result["bp"]    
        precisions = result["precisions"]
        bleu_score  = bp * math.exp(sum([math.log(p) for p in precisions[:3]]) / 3)
        result = {"bleu": bleu_score}
        prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
        result["gen_len"] = np.mean(prediction_lens)
        result = {k: round(v, 4) for k, v in result.items()}
        return result
    
    raw_dataset.map(generate_predictions, batched = True, batch_size = 100)
    predictions.map(post_processing)
    references.map(post_processing)
    references = list(map(lambda x: [x], references))
    
    
    with open("predictions.txt", "w+", encoding="utf-8") as f:
        for pred, ref in zip(predictions, references):
            bleu_score = compute_blue(predictions = [pred], references = [ref])
            f.write(f"{pred} :: {ref} :: {bleu_score['score']}\n")
    
    try:
        result = compute_bleu(preds=predictions, refs=references)
        logger.info(f"""
                    ***** eval metrics *****
                      eval_samples: {len(predictions)}
                      eval_result : {result}
                      eval_runtime: {time() - start_time} 
                    """)
    except Exception as e:
        print(e)
    
    # with open("samples_metrics.txt", mode="w+", encoding = "utf-8") as f:        
    #     for pred, ref in zip(predictions, references):
    #         bleu = compute_bleu(predictions = [pred], references = [ref])
    #         f.write(f"{pred} :: {ref} :: bleu: {bleu['score']}\n")    
        
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_repo", help="fine tuned model dir. relative dir path, or repo_id from huggingface")
    parser.add_argument("--data", help="path to test data in json format")
    parser.add_argument("--src_lang", help="ko_KR ja_XX zh_CN en_XX")
    parser.add_argument("--tgt_lang", help="ko_KR ja_XX zh_CN en_XX")
    args = parser.parse_args()
    main(args)
