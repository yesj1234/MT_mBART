import re 
from .patterns import (
    ANGLE_BRACKET_ZH,
    ENGLISH_BRACKET_ZH,
    BRACKET_PAIR_ZH_SLASH,
    ENGLISH_BRACKET_ZH_EXP,
    BRACKET_PAIR_ZH_SLASH_EXP
)
from .refine_ko import refine_ko

# 但是不是《传奇》。 :: 하지만 "레전드"가 아니고 .
# 谢谢000大凌。 :: 000대릉(大凌) 감사합니다.
# 好玩吗 好像他也是打boss（头目）那种东西。 :: 재밌어요? 이것도 보스를 타격하는 그런 게임인 것 같아요.
# 我又下來了，（怎么的）/（怎么样），我又滾。 :: 나 또 내려왔어요. 어쩔거야. 난 간다.

def refine_zh(line):
    matched = re.findall(ANGLE_BRACKET_ZH, line) # 但是不是《传奇》。 :: 하지만 "레전드"가 아니고 .
    if matched:
        line = re.sub(ANGLE_BRACKET_ZH, "", line)
    
    matched = re.findall(ENGLISH_BRACKET_ZH, line) # 好玩吗 好像他也是打boss（头目）那种东西。 :: 재밌어요? 이것도 보스를 타격하는 그런 게임인 것 같아요.
    if matched:
        for item in matched:
            print(f"item : {item}")
            selected_word = re.search(ENGLISH_BRACKET_ZH_EXP, item).groups()[0]
            print(f"selected_word : {selected_word}")
            line = line.replace(item, selected_word)
    
    matched = re.findall(BRACKET_PAIR_ZH_SLASH, line) # 我又下來了，（怎么的）/（怎么样），我又滾。 :: 나 또 내려왔어요. 어쩔거야. 난 간다. 
    if matched:
        for item in matched:
            # print(f"item : {item}")
            selected_word = re.search(BRACKET_PAIR_ZH_SLASH_EXP, item).groups()[0]
            # print(f"selected_word : {selected_word}")
            line = line.replace(item, selected_word)
            # print(f"line: {line}")
    
    return line 

def refine_zh_ko(line):
    transcription, translation = line.split(" :: ")
    transcription = refine_zh(str(transcription))
    translation = refine_ko(str(translation))
    return transcription, translation