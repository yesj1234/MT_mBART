from .patterns import (
    BRACKET_JA, 
    BRACKET_JA_ONLY, 
    BRACKET_PAIR_JA, 
    BRACKET_DOUBLE_JA, 
    BRACKET_PAIR_JA_ONLY,
    FIRST_BRACKET_FROM_PAIR,
    BRACKET_DOUBLE_JA_ONLY
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


def bracket(line):
    line = str(line)
    matched = re.findall(BRACKET_JA, line) # 「イソ」を置いて、「イソ」を置いて「スンデクッパ」を食べに行きます。
    if matched:
        for item in matched:
            item = str(item) # 「イソ」
            # logger.info(item)
            word = re.sub(BRACKET_JA_ONLY, "", item) # イソ
            word = str(word)
            line = line.replace(item, word) # 「イソ」を置いて、「イソ」を置いて「スンデクッパ」を食べに行きます。-> イソを置いて、「イソ」を置いて「スンデクッパ」を食べに行きます。
            # logger.info(line)
        return line
    else:
        return line
    
def bracket_pair(line):
    line = str(line)
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
    
def bracket_double(line): 
    line = str(line)
    matched = re.findall(BRACKET_DOUBLE_JA, line) # 『お酒モッパン』だけでもファンは喜びます。
    if matched:
        for item in matched:
            item = str(item) # 『お酒モッパン』
            # logger.info(item)
            word = re.sub(BRACKET_DOUBLE_JA_ONLY, "", item) # お酒モッパン
            # logger.info(word)
            word = str(word)
            line = line.replace(item, word) # お酒モッパンだけでもファンは喜びます。
            # logger.info(line)
        return line
    else:
        return line
def refine_ja(line):
    line = bracket(line)
    line = bracket_pair(line)
    line = bracket_double(line)
    return line 


def refine_ko_ja(line):
    transcription, translation = line.split(" :: ")
    transcription = refine_ko(transcription)
    translation = refine_ja(translation)
    return transcription, translation