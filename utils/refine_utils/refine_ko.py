from .patterns import (
    BRACKET_PAIR_KO,
    BRACKET_KO,
    BRACKET_EX,
    SPECIAL_CHARS_FOR_KO,
)
import re

def refine_ko(line):
    matched = re.findall(BRACKET_PAIR_KO, line) # (애)/(아)
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
        return line
    else:
        return line
    