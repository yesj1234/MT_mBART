from .patterns import BRACKET_PAIR_ZH, BRACKET_ZH, BRACKET_ZH_FIRST_PART
from .refine_ko import refine_ko
import re 

def refine_zh(line):
    line = str(line)
    matched = re.findall(BRACKET_PAIR_ZH, line) # （这个）（这个）
    if matched:
        for item in matched:
            item = str(item)
            print(item)
            first_part = re.match(BRACKET_ZH_FIRST_PART, item)[1] # （这个）
            first_part = str(first_part)
            print(first_part)
            first_part = re.sub(BRACKET_ZH, "", first_part) # 这个
            first_part = str(first_part)
            line = line.replace(item, first_part) # （这个）（这个） -> 这个 
            print(line)
        return line
    else:
        return line
    
def refine_ko_zh(line):
    transcription, translation = line.split(" :: ")
    transcription = refine_ko(transcription)
    translation = refine_zh(translation)
    return transcription, translation