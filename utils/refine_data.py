import os 
import re 
import argparse 
from refine_utils import (
    refine_ko_en,
    refine_ko_ja,
    refine_ko_zh,
    refine_en_ko,
    refine_ja_ko,
    refine_zh_ko
)
import logging
import sys

logger = logging.getLogger("REFINE_DATA")
logger.setLevel(logging.INFO)
streamhandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)

langs_mapper ={
    "ko_zh": refine_ko_zh,
    "ko_ja": refine_ko_ja,
    "ko_en": refine_ko_en,
    "en_ko": refine_en_ko,
    "ja_ko": refine_ja_ko,
    "zh_ko": refine_zh_ko
}
file_to_refine = ["test", "train", "validation"]

def main(args):
    for root, _dir, files in os.walk(args.tsv_splits_dir):
        for file in files:
            fname, ext = os.path.splitext(file)
            if ext == ".tsv" and fname in file_to_refine:
                with open(os.path.join(root, file), "r+", encoding="utf-8") as original_file, open(os.path.join(root, f"{fname}_refined.tsv"), "w+", encoding="utf-8") as refined_file:
                    lines = original_file.readlines()
                    new_lines = []
                    cnt = 0
                    for line in lines: 
                        try:
                            transcription, translation = langs_mapper[args.langs](line)
                            new_lines.append(f"{transcription} :: {translation}")
                        except Exception as e:
                            logger.warning(e)
                            logger.warning(file)
                            cnt += 1
                            pass 
                    for l in new_lines:
                        refined_file.write(l) 
                    logger.info(cnt)  
                        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tsv_splits_dir", help="mt_split 디렉토리 경로")
    parser.add_argument("--langs", help="ko_en, ko_ja, ko_zh, en_ko, ja_ko, zh_ko")
    args = parser.parse_args()
    main(args)