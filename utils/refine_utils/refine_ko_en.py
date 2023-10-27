from .refine_ko import refine_ko
from .patterns import (
    BRACKET_PAIR_EN, 
    FIRST_BRACKET_FROM_PAIR, 
    BRACKET_PAIR_EN_ONLY, 
    BRACKET_PAIR_WITH_SLASH_EN,
    REMAINING_BRACKET_TO_REMOVE
)
import re

def refine_en(line):
    matched = re.findall(BRACKET_PAIR_EN, line) # (buku)(much)
    if matched:
        for item in matched:
            word = re.match(FIRST_BRACKET_FROM_PAIR, item)[0]
            word = re.sub(BRACKET_PAIR_EN_ONLY, "", word)
            line = line.replace(item, word)
    
    matched = re.findall(BRACKET_PAIR_WITH_SLASH_EN, line) # (buku)/(much)
    if matched:
        for item in matched:
            # print(f"item: {item}")
            first_word = item.split(")")[0][1:]
            # print(f"first_word: {first_word}")
            line = line.replace(item, first_word)
    
    # remove remaining parenthesis 
    matched = re.findall(REMAINING_BRACKET_TO_REMOVE, line)
    if matched:
        line = re.sub(REMAINING_BRACKET_TO_REMOVE, "", line)
    return line 



def refine_ko_en(line):
    transcription, translation = line.split(" :: ")
    transcription = refine_ko(transcription)
    translation = refine_en(translation)
    return transcription, translation