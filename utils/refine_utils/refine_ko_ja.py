from .patterns import (
    BRACKET_PAIR_JA, 
    BRACKET_PAIR_JA_ONLY,
    FIRST_BRACKET_FROM_PAIR,
    BRACKET_RIGHT_ANGLE_JA,
    BRACKET_PAIR_SECOND_JA,
    SPECIAL_CHARS_FOR_JA
)
from .refine_ko import refine_ko
import re 
import logging
import sys 
logger = logging.getLogger("REFINE_JA")
logger.setLevel(logging.INFO)
streamhandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)




def bracket_right_angle(line):
    matched = re.findall(BRACKET_RIGHT_ANGLE_JA, line)
    if matched:
        for item in matched:
            line = line.replace(item, "")
        return line
    return line 
    
def bracket_pair(line):
    matched = re.findall(BRACKET_PAIR_JA, line) # 文字通りオム(エッセンス)(essence)男性向けの(エッセンス)(essence)を用意しております。。
    if matched:
        for item in matched:
            item = str(item) # (エッセンス)(essence)
            # logger.info(item)
            word = re.match(FIRST_BRACKET_FROM_PAIR, item)[0] # (エッセンス)
            # logger.info(word)
            word = re.sub(BRACKET_PAIR_JA_ONLY, "", word) # エッセンス
            # logger.info(word)
            word = str(word)
            line = line.replace(item, word) # 文字通りオム(エッセンス)(essence)男性向けの(エッセンス)(essence)を用意しております。。 -> 文字通りオムエッセンス男性向けのエッセンスを用意しております。。
            # logger.info(line)
        return line
    else:
        return line

def bracket_pair_second(line):
    matched = re.findall(BRACKET_PAIR_SECOND_JA, line) # (これ)(これ) 혹은 (私が)(本当に) 같거나 다르거나 둘다 2번째 캡처 그룹을 사용할 것.
    if matched:
        for item in matched:
            try:
                # print(f"line: {line}")
                _, second_one = item
                # print(f"second_one: {second_one}")
                target = re.search(BRACKET_PAIR_SECOND_JA, line).group()
                # print(f"target: {target}")
                line = line.replace(target, second_one)
            except Exception as e:
                pass
    return line 

def special_chars(line):
    matched = re.findall(SPECIAL_CHARS_FOR_JA, line)
    if matched:
        for item in matched:
            line = line.replace(item, "")
    return line 

def refine_ja(line):
    line = bracket_right_angle(line)
    line = bracket_pair(line)
    line = bracket_pair_second(line)
    line = special_chars(line)
    return line 


def refine_ko_ja(line):
    transcription, translation = line.split(" :: ")
    transcription = refine_ko(str(transcription))
    translation = refine_ja(str(translation))
    return transcription, translation