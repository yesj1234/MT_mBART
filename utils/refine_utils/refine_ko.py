from .patterns import (
    BRACKET_KO,
    BRACKET_EX,
    BRACKET_PAIR_KO_PRONOUNCE,
    BRACKET_PAIR_KO_FAKE
)
import re

def refine_ko(line):
    matched = re.findall(BRACKET_PAIR_KO_PRONOUNCE, line) # (애)/(아)
    if matched:
        for item in matched:
            try:
                first_part = item.split("/")[0] # (애)
                first_part = re.sub(BRACKET_KO, "", first_part) # (애) -> 애
                line = line.replace(item, first_part) # (애)/(아) -> 애 
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
    matched = re.findall(BRACKET_PAIR_KO_FAKE) # (로제)/(rose)
    if matched:
        for item in matched:
            try:
                first_part = item.split("/")[0] # (로제)
                first_part = re.sub(BRACKET_KO, "", first_part) # (로제) -> 애
                line = line.replace(item, first_part) # (로제)/(rose) -> 로제 
            except Exception as e:
                print(e)
                pass
        return line
    else:
        return line
    