import re

## 한국어
BRACKET_PAIR_KO = re.compile("\([^\/]+\)\/\([^\/\(\)]+\)") # 1. (이거)/(요거) 모양 패턴
BRACKET_KO = re.compile("[\(\)]") # 2. (문자) 모양 패턴
BRACKET_EX = re.compile("\/\([^\/]+\)") # 뭣뭣/(무엇무엇) 모양 패턴
SPECIAL_CHARS_FOR_KO = re.compile("[a-z,?!%'~:/+\-*().·@]") # 한글 이외의 특수 기호들 [a-z,?!%'~:/+\-*().·@] 패턴 




## 중국어 
open_bracket = chr(65288)
close_bracket = chr(65289)
BRACKET_PAIR_ZH = re.compile(f"{open_bracket}.+?{close_bracket}{open_bracket}.+?{close_bracket}") # （这个）（这个） 모양의 패턴 , 嗯，我好像有点(摄像机)(camera)恐惧症。 모양의 패턴들로부터 앞의 것 만 선택하기 위함. 
BRACKET_ZH = re.compile(f"[{open_bracket}{close_bracket}]") # （） char code 65288, 65289 괄호매칭
BRACKET_ZH_FIRST_PART = re.compile(f"^{open_bracket}.+?{close_bracket}") # （.）（.） 중 첫번째 괄호 매칭
BRACKET_PAIR_ZH_SLASH = re.compile(f"{open_bracket}[^\/]+{close_bracket}\/{open_bracket}[^\/{open_bracket}{close_bracket}]+{close_bracket}")

## 일본어
bracket_ja = chr
BRACKET_JA = re.compile("「.+?」")   # 「イソ」
BRACKET_JA_ONLY = re.compile("[「」]") # 「」
BRACKET_PAIR_JA = re.compile("\(.+?\)\(.+?\)") # 文字通りオム(エッセンス)(essence)男性向けの(エッセンス)(essence)を用意しております。
BRACKET_PAIR_JA_ONLY = re.compile("[\(\)]")
FIRST_BRACKET_FROM_PAIR = re.compile("\(.+?\)")
BRACKET_DOUBLE_JA = re.compile("『.+?』")   # 『家族愛ウォーキング大会』
BRACKET_DOUBLE_JA_ONLY = re.compile("[『』]") # matching 『』


##영어
BRACKET_PAIR_EN = re.compile("\(.+?\)\(.+?\)") # (head)(head)
BRACKET_PAIR_EN_ONLY = re.compile("[\(\)]")
