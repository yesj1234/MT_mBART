import re
from .patterns import (
    BRACKET_PAIR_WITH_SLASH_JA,
    slash_ja,
    open_bracket,
    close_bracket
)
from .refine_ko import refine_ko

def refine_ja(line):
    matched = re.findall(BRACKET_PAIR_WITH_SLASH_JA, line) # （人んち）／（人の家） 혹은 (ほんまに)/(本当に) 
    if matched:
        for item in matched:
            try:
                if slash_ja in item:
                    first_part = item.split("/")[0] # 
                    first_part = re.sub(f"[(){open_bracket}{close_bracket}]", "", first_part) # 
                    line = line.replace(item, first_part) # 
                elif "/" in item:
                    first_part = item.split("/")[0] # 
                    first_part = re.sub(f"[(){open_bracket}{close_bracket}]", "", first_part) # 
                    line = line.replace(item, first_part) # 
            except Exception as e:
                print(e)
                pass
    return line 

def refine_ja_ko(line):
    transcription, translation = line.split(" :: ")
    transcription = refine_ja(str(transcription))
    translation = refine_ko(str(translation))
    return transcription, translation