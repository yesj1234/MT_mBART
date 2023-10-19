from .refine_ko import refine_ko
from .patterns import BRACKET_PAIR_EN, FIRST_BRACKET_FROM_PAIR, BRACKET_PAIR_EN_ONLY
import re

def refine_en(translation):
    matched = re.findall(BRACKET_PAIR_EN, translation)
    if matched:
        for item in matched:
            word = re.match(FIRST_BRACKET_FROM_PAIR, item)[0]
            word = re.sub(BRACKET_PAIR_EN_ONLY, "", word)
            translation = translation.replace(item, word)
        return translation 
    else:
        return translation
def refine_ko_en(line):
    transcription, translation = line.split(" :: ")
    transcription = refine_ko(transcription)
    translation = refine_en(translation)
    return transcription, translation