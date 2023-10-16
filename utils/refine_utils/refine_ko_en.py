from .refine_ko import refine_ko
def refine_en(line):
    return line
def refine_ko_en(line):
    transcription, translation = line.split(" :: ")
    transcription = refine_ko(transcription)
    translation = refine_en(translation)
    return transcription, translation