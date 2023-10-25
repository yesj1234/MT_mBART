import re 
from .refine_ko import refine_ko

def refine_en(line):
    return line

def refine_en_ko(line):
    transcription, translation = line.split(" :: ")
    transcription = refine_en(transcription)
    translation = refine_ko(translation)
    return transcription, translation