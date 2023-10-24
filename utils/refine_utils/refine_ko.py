from .patterns import (
    BRACKET_KO,
    BRACKET_EX,
    BRACKET_PAIR_KO_PRONOUNCE,
    BRACKET_PAIR_KO_FAKE,
    BRACKET_PAIR_KO_PRONOUNCE_NO_SLASH,
    BRACKET_PAIR_KO_FAKE_NO_SLASH,
    BRACKET_WORD_PICKING
)
import re

def refine_ko(line):
    matched = re.findall(BRACKET_PAIR_KO_PRONOUNCE, line) # (고것도)/(그것도)
    if matched:
        for item in matched:
            try:
                first_part = item.split("/")[1] # (그것도)
                first_part = re.sub(BRACKET_KO, "", first_part) # (그것도) -> 그것도
                line = line.replace(item, first_part) # (고것도)/(그것도) -> 그것도 
            except Exception as e:
                print(e)
                pass
    else:
        pass
    
    matched = re.findall(BRACKET_EX, line) # 뭣뭣/(무엇무엇)
    if matched:
        for item in matched:
            first_part = item.split("/")[1] # 무엇무엇 선택 
            line = line.replace(item, first_part) # 뭣뭣/(뭐뭐) -> 무엇무엇
    else:
        pass
    
    matched = re.findall(BRACKET_PAIR_KO_FAKE, line) # (로제)/(rose)
    if matched:
        for item in matched:
            try:
                first_part = item.split("/")[0] # (로제)
                first_part = re.sub(BRACKET_KO, "", first_part) # (로제) -> 애
                line = line.replace(item, first_part) # (로제)/(rose) -> 로제 
            except Exception as e:
                print(e)
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
            except Exception as e:
                print(e)
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
            except Exception as e:
                print(e)
                pass
    
    return line 