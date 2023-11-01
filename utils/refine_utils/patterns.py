import re


##### 중국어, 일본어 공통 #####
open_bracket = chr(65288)
close_bracket = chr(65289)

####### 한국어 #######
BRACKET_PAIR_KO_PRONOUNCE = re.compile("\(\s*?[^a-zA-Z]+?\s*?\)\s*?\/\s*?\(\s*?[^a-zA-Z]+?\s*?\)") # 1. (그래가지고)/(그래서) 혹은 (고것도)/(그것도)
BRACKET_PAIR_KO_FAKE = re.compile("\([\sㄱ-ㅎㅏ-ㅣ가-힣]+?\)\s*?\/\s*?\([\sa-zA-Z]+?\)") # 1. (로제)/(rose) 모양 패턴
BRACKET_PAIR_KO_FAKE_REVERSE = re.compile("\([\sa-zA-Z]+?\)\s*?\/\s*?\([\sㄱ-ㅎㅏ-ㅣ가-힣]+?\)")  
BRACKET_KO_FAKE = re.compile("[ㄱ-ㅎ가-힣ㅏ-ㅣ]+?\s*?\(\s*?[a-zA-Z]+?\s*?\)") # 로제(rose)
BRACKET_KO = re.compile("[\(\)]") # 2. (문자) 에서 () 를 지우기 위한 패턴

BRACKET_PAIR_KO_PRONOUNCE_NO_SLASH = re.compile("\([^a-zA-Z]+?\)\([^a-zA-Z]+?\)") # (요)(이)
BRACKET_PAIR_KO_FAKE_NO_SLASH = re.compile("\(.+?\)\([\?\&\s0-9a-zA-Z\'\"\-]+?\)") # (로제)(rose)
BRACKET_WORD_PICKING = re.compile("\(.+?\)") # (요)(이) -> (요) 와 (이) 를 따로 찾기 위함. 

BRACKET_EX = re.compile("[ㄱ-ㅎ가-힣ㅏ-ㅣ]+?\s*?\/\([\sㄱ-ㅎ가-힣ㅏ-ㅣ]\)") # 뭣뭣/(무엇무엇) 
BRACKET_EX_WITHOUT_SLASH = re.compile("[ㄱ-ㅎ가-힣ㅏ-ㅣ]+?\s*?\([\sㄱ-ㅎ가-힣ㅏ-ㅣ]\)") # 모모모(뭐뭐뭐) 

REMAINING_BRACKET_TO_REMOVE_KO = re.compile("\([ㄱ-ㅎ가-힣ㅏ-ㅣ\s]+?\)")
 
SPECIAL_CHARS_FOR_KO = re.compile("[,?!%'~:/+\-*().·@]") # 한글 이외의 특수 기호들 패턴 




###### 중국어 ######
angle_bracket_open = chr(12299)
angle_bracket_close = chr(12298)
comma_zh = chr(65292)
question_zh = chr(65311)
exclamation_zh = chr(65281)
BRACKET_PAIR_ZH = re.compile(f"[{open_bracket}\(].+?[{close_bracket}\)][{open_bracket}\(][^a-zA-Z]+?[{close_bracket}\)]") # （这个）（这个） 모양의 패턴 , 嗯，我好像有点(摄像机)(camera)恐惧症。 모양의 패턴들로부터 앞의 것 만 선택하기 위함. 
BRACKET_ZH = re.compile(f"[\(\){open_bracket}{close_bracket}]") # （） char code 65288, 65289 괄호매칭
BRACKET_ZH_FIRST_PART = re.compile(f"^[{open_bracket}\(].+?[{close_bracket}\)]") # （.）（.） 중 첫번째 괄호 매칭

BRACKET_PAIR_ZH_SLASH = re.compile(f"[{open_bracket}\(][^\/]+?[{close_bracket}\)]\/[{open_bracket}\(][^\/{open_bracket}{close_bracket}]+?[{close_bracket}\)]")
BRACKET_PAIR_ZH_SLASH_EXP = re.compile(f"[{open_bracket}\(][^\/]+?[{close_bracket}\)]\/[{open_bracket}\(]([^\/{open_bracket}{close_bracket}]+?)[{close_bracket}\)]")

BRACKET_PAIR_ZH_FAKE = re.compile(f"[\({open_bracket}].+?[\){close_bracket}][\({open_bracket}][a-zA-Z\s]+?[\){close_bracket}]")

ANGLE_BRACKET_ZH = re.compile(f"[{angle_bracket_close}{angle_bracket_open}]")

ENGLISH_BRACKET_ZH = re.compile(f"[a-zA-Z0-9]+?\s*?[{open_bracket}\(]\s*?.+?\s*?[{close_bracket}\)]") # boss（头目）
ENGLISH_BRACKET_ZH_EXP = re.compile(f"[a-zA-Z0-9]+?\s*?[{open_bracket}\(]\s*?(.+?)\s*?[{close_bracket}\)]") 

SPECIAL_CHARS_FOR_ZH = re.compile(f"[。,?.{comma_zh}{question_zh}!{exclamation_zh}]")


###### 일본어 ######
slash_ja = chr(65295) # "／"
BRACKET_RIGHT_ANGLE_JA = re.compile("[\「\」\『\』]")   # 「」,『』 PATTERN. Simply remove the symbol.

BRACKET_PAIR_JA = re.compile("\(\s*?.+?\s*?\)\s*?\(\s*?[a-zA-Z.\?\']+?\s*?\)") # 文字通りオム(エッセンス)(essence)男性向けの(エッセンス)(essence)を用意しております。
BRACKET_PAIR_JA_ONLY = re.compile("[\(\)]")
FIRST_BRACKET_FROM_PAIR = re.compile("\(.+?\)")

BRACKET_PAIR_SECOND_JA = re.compile(f"[\({open_bracket}]\s*?([^a-zA-Z\({open_bracket}]+?)\s*?[\){close_bracket}]\s*?[\({open_bracket}]\s*?([^a-zA-Z]+?)\s*?[\){close_bracket}]")

BRACKET_PAIR_WITH_SLASH_JA = re.compile(f"[\({open_bracket}]\s*?([^a-zA-Z\({open_bracket}]+?)\s*?[\){close_bracket}]\s*?[\/{slash_ja}]\s*?[\({open_bracket}]\s*?([^a-zA-Z]+?)\s*?[\){close_bracket}]")
BRACKET_PAIR_WITH_SLASH_JA_NO_GROUP = re.compile(f"[\({open_bracket}]\s*?[^a-zA-Z\({open_bracket}]+?\s*?[\){close_bracket}]\s*?[\/{slash_ja}]\s*?[\({open_bracket}]\s*?[^a-zA-Z]+?\s*?[\){close_bracket}]")
# (これ)(これ) / (そのように)(そのように) 
# (私が)(本当に) / (大目に見ると)(足を踏み入れたら) 

SPECIAL_CHARS_FOR_JA = re.compile(f"[。,?.{comma_zh}{question_zh}!{exclamation_zh}]")

##영어
BRACKET_PAIR_EN = re.compile("\(\s*?.+?\s*?\)\s*?\(\s*?.+?\s*?\)") # (head)(head)
BRACKET_PAIR_EN_ONLY = re.compile("[\(\)]")

BRACKET_PAIR_WITH_SLASH_EN = re.compile("\([\sa-zA-Z0-9\?\']+?\)\s*?\/\s*?\([\sa-zA-Z0-9\?\']+?\)") # (grandpa)/(grandfather)
REMAINING_BRACKET_TO_REMOVE = re.compile("[\(\)]")