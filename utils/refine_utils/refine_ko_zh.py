from .patterns import (
    BRACKET_PAIR_ZH, 
    BRACKET_ZH, 
    BRACKET_ZH_FIRST_PART, 
    BRACKET_PAIR_ZH_FAKE,
    BRACKET_PAIR_ZH_SLASH, 
    SPECIAL_CHARS_FOR_ZH
)
from .refine_ko import refine_ko
import re 

def refine_zh(line):
    line = str(line)
    matched = re.findall(BRACKET_PAIR_ZH, line) # （这个）（这个）
    if matched:
        for item in matched:
            item = str(item)
            print(item)
            first_part = re.match(BRACKET_ZH_FIRST_PART, item)[0] # （这个）
            first_part = str(first_part)
            print(first_part)
            first_part = re.sub(BRACKET_ZH, "", first_part) # 这个
            first_part = str(first_part)
            line = line.replace(item, first_part) # （这个）（这个） -> 这个 
            print(line)
    
    matched = re.findall(BRACKET_PAIR_ZH_FAKE, line) # (腺苷)(adenosine)
    if matched:
        for item in matched:
            first_part = str(re.match(BRACKET_ZH_FIRST_PART, item)[0]) # (腺苷)
            first_part = re.sub(BRACKET_ZH, "", first_part)
            line = line.replace(item, first_part)
    
    matched = re.findall(BRACKET_PAIR_ZH_SLASH, line)
    if matched:
        for item in matched:
            first_part = str(re.match(BRACKET_ZH_FIRST_PART, item)[0])
            first_part = re.sub(BRACKET_ZH, "", first_part)
            line = line.replcae(item, first_part)

    matched = re.findall(SPECIAL_CHARS_FOR_ZH, line)
    if matched:
        for item in matched:
            line = line.replace(item, "")
    return line 


    
def refine_ko_zh(line):
    transcription, translation = line.split(" :: ")
    transcription = refine_ko(transcription)
    translation = refine_zh(translation)
    return transcription, translation