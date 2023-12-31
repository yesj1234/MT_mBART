from .patterns import (
    BRACKET_KO,
    BRACKET_EX,
    BRACKET_PAIR_KO_PRONOUNCE,
    BRACKET_PAIR_KO_FAKE,
    BRACKET_PAIR_KO_PRONOUNCE_NO_SLASH,
    BRACKET_PAIR_KO_FAKE_NO_SLASH,
    BRACKET_WORD_PICKING,
    BRACKET_KO_FAKE,
    SPECIAL_CHARS_FOR_KO,
    REMAINING_BRACKET_TO_REMOVE_KO,
    BRACKET_PAIR_KO_FAKE_REVERSE,
    BRACKET_EX_WITHOUT_SLASH,
    BRACKET_PAIR_KO_FAKE_NO_SLASH_REVERSE
)
import re
import traceback

def refine_ko(line):
    matched = re.findall(BRACKET_PAIR_KO_PRONOUNCE, line) # (고것도)/(그것도)
    if matched:
        for item in matched:
            try:
                first_part = item.split("/")[1] # (그것도)
                first_part = re.sub(BRACKET_KO, "", first_part) # (그것도) -> 그것도
                line = line.replace(item, first_part) # (고것도)/(그것도) -> 그것도 
            except Exception:
                print(traceback.format_exc())
                pass
    
    matched = re.findall(BRACKET_EX, line) # 뭣뭣/(무엇무엇)
    if matched:
        for item in matched:
            second_part = item.split("/")[1] # 무엇무엇 선택 
            second_part = re.sub("\(\)", "", second_part)
            line = line.replace(item, second_part) # 뭣뭣/(뭐뭐) -> 무엇무엇
    
    matched = re.findall(BRACKET_EX_WITHOUT_SLASH, line) # 모모모(뭐뭐뭐)
    if matched:
        for item in matched:
            second_part = item.split("(")[1]
            second_part = re.sub("\)", "", second_part)
            line = line.replace(item, second_part)
    
    matched = re.findall(BRACKET_PAIR_KO_FAKE, line) # (로제)/(rose)
    if matched:
        for item in matched:
            try:
                # print(f"formatting item: {item}")
                first_part = item.split("/")[0] # (로제)
                # print(f"first_part: {first_part}")
                first_part = re.sub(BRACKET_KO, "", first_part) # (로제) -> 로제
                line = line.replace(item, first_part) # (로제)/(rose) -> 로제 
                # print(f"formatted line: {line}")
            except Exception:
                print(traceback.format_exc())
                pass
    
    matched = re.findall(BRACKET_PAIR_KO_FAKE_REVERSE, line) # (rose)/(로제)
    if matched:
        for item in matched:
            try:
                second_part = item.split("/")[1]
                second_part = re.sub(BRACKET_KO, "", second_part)
                line = line.replace(item, second_part)
            except Exception:
                print(traceback.format_exc())
                pass

    matched = re.findall(BRACKET_PAIR_KO_PRONOUNCE_NO_SLASH, line) # (요)(이)
    if matched:
        for item in matched:
            try:
                selected_word = re.findall(BRACKET_WORD_PICKING, item)[1]
                # print(f"selected_word from pronounce pattern: {selected_word}")
                selected_word = re.sub(BRACKET_KO, "", selected_word)
                line = line.replace(item, selected_word)
                # print(f"line: {line}")
            except Exception:
                print(traceback.format_exc())
                pass
            
    matched = re.findall(BRACKET_PAIR_KO_FAKE_NO_SLASH, line) # (로제)(rose)
    if matched:
        for item in matched:
            try:
                selected_word = re.findall(BRACKET_WORD_PICKING, item)[0]
                # print(f"selected_word from fake pattern: {selected_word}")
                selected_word = re.sub(BRACKET_KO, "", selected_word)
                line = line.replace(item, selected_word)
                # print(f"line: {line}")
            except Exception:
                print(traceback.format_exc())
                pass
    
    matched = re.findall(BRACKET_PAIR_KO_FAKE_NO_SLASH_REVERSE, line) # (rose)(로제)
    if matched:
        for item in matched:
            try:
                selected_word = re.findall(BRACKET_WORD_PICKING, item)[1]
                # print(f"selected_word from fake pattern: {selected_word}")
                selected_word = re.sub(BRACKET_KO, "", selected_word)
                line = line.replace(item, selected_word)
                # print(f"line: {line}")
            except Exception:
                print(traceback.format_exc())
                pass
            
    matched = re.findall(BRACKET_KO_FAKE, line) # 로제(rose)
    if matched:
        for item in matched:
            try:
                # print(item)
                selected_word = item.split("(")[0]
                # print(f"selected_word: {selected_word}")
                line = line.replace(item, selected_word)
            except Exception:
                print(traceback.format_exc())
                pass
    
    matched = re.findall(REMAINING_BRACKET_TO_REMOVE_KO,line)# 남아 있는 괄호들 제거
    if matched:
        # print(f"matched: {matched}")
        line = re.sub(REMAINING_BRACKET_TO_REMOVE_KO, "", line)
        # print(f"line: {line}")
    
    matched = re.findall(SPECIAL_CHARS_FOR_KO, line)
    if matched:
        for item in matched:
            try:
                line = line.replace(item, "")
            except Exception:
                print(traceback.format_exc())
                pass 
    return line 