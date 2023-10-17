import re 
from .patterns import BRACKET_PAIR_ZH, BRACKET_ZH_FIRST_PART, BRACKET_PAIR_ZH_SLASH, BRACKET_ZH

def refine_ko(line):
    return line
def refine_zh(line):
    line = str(line)
    matched = re.findall(BRACKET_PAIR_ZH, line) # （这个）（这个）
    if matched:
        for item in matched:
            item = str(item)
            print(item)
            first_part = re.match(BRACKET_ZH_FIRST_PART, item)[0] # （这个）
            first_part = str(first_part)
            print(first_part)
            first_part = re.sub(BRACKET_ZH, "", first_part) # 这个
            first_part = str(first_part)
            line = line.replace(item, first_part) # （这个）（这个） -> 这个 
            print(line)
    matched = re.findall(BRACKET_PAIR_ZH_SLASH, line) # （这个）/（这个）
    if matched:
        for item in matched:
            try:
                first_part = item.split("/")[0] # （这个）
                first_part = re.sub(BRACKET_ZH, "", first_part) # （这个） -> 这个
                line = line.replace(item, first_part) # （这个）/（这个） -> 这个
            except Exception as e:
                print(e)
                pass
            return line
    else:
        return line


def refine_zh_ko(line):
    transcription, translation = line.split(" :: ")
    transcription = refine_zh(transcription)
    translation = refine_ko(translation)
    return transcription, translation