import re 


def refine_ko(line):
    BRACKET_PATTERN = re.compile("\(.+?\)")
    matched = re.findall(BRACKET_PATTERN, line)
    if matched:
        for item in matched:
            line = line.replace(item, "")
    return line 

def refine_en(line):
    return line

def refine_en_ko(line):
    transcription, translation = line.split(" :: ")
    transcription = refine_en(transcription)
    translation = refine_ko(translation)
    return transcription, translation