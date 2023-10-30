import re
from .patterns import (
    BRACKET_PAIR_WITH_SLASH_JA,
    BRACKET_PAIR_WITH_SLASH_JA_NO_GROUP,
    slash_ja,
    open_bracket,
    close_bracket
)
from .refine_ko import refine_ko

def refine_ja(line):
    matched = re.findall(BRACKET_PAIR_WITH_SLASH_JA, line) # （人んち）／（人の家） 혹은 (ほんまに)/(本当に) 
    if matched:
        print(f"matched: {matched}")
        for item in matched:
            try: 
                matched_part = re.search(BRACKET_PAIR_WITH_SLASH_JA_NO_GROUP, line).group()
                # print(f"item in matched: {item}")
                # print(f"matched_part: {matched_part}")
                _, selected_one = item
                line = line.replace(matched_part, selected_one)
                # print(f"line: {line}")
            except Exception as e:
                print(e)
                pass 
    return line 

def refine_ja_ko(line):
    transcription, translation = line.split(" :: ")
    transcription = refine_ja(str(transcription))
    translation = refine_ko(str(translation))
    return transcription, translation