import re 
import traceback
from .refine_ko import refine_ko
from .patterns import (
    BRACKET_PAIR_WITH_SLASH_EN,
    BRACKET_WITH_KOREAN_EN,
    BRACKET_PAIR_ABBREVIATION_EN
)


def refine_en(line):
    matched = re.findall(BRACKET_PAIR_WITH_SLASH_EN, line)
    if matched:
        try:
            for item in matched:
                second_part = item.split("/")[1]
                second_part = re.sub("()", "", second_part)
                line = line.replace(item, second_part)
        except Exception:
            print(traceback.format_exc())
            pass
            
    matched = re.findall(BRACKET_WITH_KOREAN_EN, line)
    if matched:
        try:
            for item in matched:
                line = line.replace(item, "")
        except Exception:
            print(traceback.format_exc())
            pass
            
    matched = re.findall(BRACKET_PAIR_ABBREVIATION_EN, line)
    if matched:
        try:
            for item in matched:
                groups = re.findall("\(.+?\)", item)
                if groups:
                    second_part = groups[1]
                    second_part = re.sub("()", "", second_part)
                    line = line.replace(item, second_part)
        except Exception:
            print(traceback.format_exc())
            pass
        
    return line

def remove_space(line):
    if not line: 
        return ""
    line = line.split()
    line = " ".join(line)
    return line

def refine_en_ko(line):
    transcription, translation = line.split(" :: ")
    transcription = refine_en(transcription)
    translation = refine_ko(translation)
    transcription = remove_space(transcription)
    translation = remove_space(translation)
    return transcription, translation