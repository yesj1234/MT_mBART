import os 
import re 
import argparse 
from refine_utils.refine_zh import refine_zh
from refine_utils.refine_ko import refine_ko

def main(args):
    for root, _dir, files in os.walk(args.tsv_splits_dir):
        for file in files:
            fname, ext = os.path.splitext(file)
            if ext == ".tsv":
                with open(os.path.join(root, file), "r+", encoding="utf-8") as original_file, open(os.path.join(root, f"{fname}_refined.tsv"), "w+", encoding="utf-8") as refined_file:
                    lines = original_file.readlines()
                    new_lines = []
                    cnt = 0
                    if args.langs == "ko-zh":
                        # ()/() 모양 패턴 제거
                        for line in lines: 
                            try:
                                transcription, translation = line.split(" :: ")
                                transcription = refine_ko(transcription)
                                translation = refine_zh(translation)
                                new_lines.append(f"{transcription} :: {translation}")
                            except Exception as e:
                                print(e)
                                print(file)
                                print(transcription)
                                print(translation)
                                cnt += 1
                                pass 
                        for l in new_lines:
                            refined_file.write(l) 
                        print(cnt)   
                        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tsv_splits_dir", help="asr_splits 디렉토리 경로")
    parser.add_argument("--langs", help="ko-en, ko-ja, ko-zh, en-ko, ja-ko, zh-ko")
    args = parser.parse_args()
    main(args)