import argparse
import torch
import librosa
from tqdm import tqdm
import logging 
import sys
import re 
from time import time 

from transformers import (
    MBartForConditionalGeneration, 
    MBart50TokenizerFast
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
logger.setLevel(logging.INFO)

SACREBLEU_TOKENIZE = {
    "ko_KR": "ko-mecab",
    "ja_XX": "ja-mecab",
    "en_XX": "13a",
    "zh_CN": "zh"
}



def main(args):
    start_time = time()

    if args.test_dataset:
        test_dataset = load_dataset("json", data_files = args.test_dataset, field="translation")["train"]
    if args.validation_dataset:
        validation_dataset = load_dataset("json", data_files = args.validation_dataset, field = "translation")["train"]
    
    # raw_dataset = raw_dataset.map(remove_special_characters, num_proc = 8, desc="remove special chars")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    model = MBartForConditionalGeneration.from_pretrained(args.model_repo)
    tokenizer = MBart50TokenizerFast.from_pretrained(args.model_repo)
    src_lang = args.src_lang
    tgt_lang = args.tgt_lang
    metric = evaluate.load("sacrebleu")
    references_temp = []
    predictions_temp = []
    
    def generate_predictions(batch):
        src_text = batch["en"]
        model_inputs = tokenizer(src_text, return_tensors="pt").to(device)
        with torch.no_grad():
            generated_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.lang_code_to_id[src_lang]).to(device)
        prediction = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        return prediction
    
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
    
    logger.info("***** Running Evaluation *****")
    for batch in tqdm(validation_dataset):
        try:
            predicted_sentence = generate_predictions(batch)
            predicted_sentence = predicted_sentence[0].strip()
            predictions_temp.append(predicted_sentence)
            references_temp.append(batch[tgt_lang])
        except Exception as e:
            logger.warning(e)
            pass
        
    references = []
    predictions = []
    
    logger.info("***** Simple postprocessing *****")
    for i, pair in tqdm(enumerate(zip(predictions_temp, references_temp))):
        prediction, reference =pair
        prediction = prediction.strip()
        prediction = "".join(list(prediction)).lower()
        reference = reference.strip()
        reference = "".join(list(reference)).lower()
    
    with open("predictions.txt", "w+", encoding="utf-8") as f:
        for prediction, reference in zip(predictions, references):
            f.write(f"{prediction} :: {reference}\n")
    
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
    
    with open("samples_metrics.txt", mode="w+", encoding = "utf-8") as f:        
        for pred, ref in zip(predictions, references):
            bleu = compute_bleu(predictions = [pred], references = [ref])
            f.write(f"{pred} :: {ref} :: bleu: {bleu['score']}\n")    
        
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", help="fine tuned model dir. relative dir path, or repo_id from huggingface")
    parser.add_argument("--load_script", help="script used for loading dataset for computing metrics.")
    parser.add_argument("--lang", help="ko ja zh en")
    args = parser.parse_args()
    main(args)
