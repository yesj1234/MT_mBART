########################################################################################################################################################################
# {
#     "fi_sound_filename": "54_106_11.60_19.34.wav",
#     "fi_sound_filepath": "https://objectstorage.ap-seoul-1.oraclecloud.com/n/cnb97trxvnun/b/clive-resource/o/output/한국어_영어/원천데이터/교육/54/54_106_11.60_19.34.wav",
#     "tc_text": "네  유치원 교육과정 A형 어 저희가 보도록 하겠습니다. 2013학년도 유치원 교육과정 A입니다.",
#     "tl_trans_lang": "영어",
#     "tl_trans_text": "We'll take a look at Kindergarten Curriculum Type A. This is kindergarten Curriculum A for the 2013 school year.",
# }
import json
import os
import argparse
import numpy as np
import re
import logging
logger = logging.getLogger("splitting_logger")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
logger.addHandler(streamHandler)

def get_neccesary_info(json_file):
    json_data = json.load(json_file)
    transcription = json_data["tc_text"]
    transcription = re.sub("\n", " ", transcription)
    translation = json_data["tl_trans_text"]
    translation = re.sub("\n", " ", translation)
    return transcription, translation

def get_pairs(dir_path, ratio = 1.0):
    pairs = []
    for root, dirs, files in os.walk(dir_path):
        if dirs:
            for dir in dirs:
                logger.info(f"json files from {os.path.join(root, dir)}")
                files = os.listdir(os.path.join(root, dir))
                if files:
                    for file in files:
                        _, ext = os.path.splitext(file)
                        if ext == ".json":
                            with open(os.path.join(root, dir, file), "r", encoding="utf-8") as json_file:
                                try:
                                    transcription, translation = get_neccesary_info(
                                        json_file)
                                    pairs.append((transcription, translation))
                                except Exception as e:
                                    logger.warning(e)
                                    logger.warning(file)
    np.random.shuffle(pairs) # shuffle in-place and return none.
    maximum_index = int(len(pairs) * ratio)
    return pairs[:maximum_index] # return the given ratio. defaults to 100%.

def split_data(pairs):
    transcriptions = list(map(lambda x:x[0], pairs))
    translations = list(map(lambda x:x[1], pairs))
    transcription_train, transcription_validate, transcription_test = np.split(
        transcriptions, [int(len(transcriptions)*0.8), int(len(transcriptions)*0.9)])
    translation_train, translation_validate, translation_test = np.split(translations, [
                                                                         int(len(translations)*0.8), int(len(translations)*0.9)])
    assert len(transcription_train) == len(
        translation_train), "train split 길이 안맞음."
    assert len(transcription_test) == len(
        translation_test), "test split 길이 안맞음."
    assert len(transcription_validate) == len(
        translation_validate), "validate split 길이 안맞음."
    return transcription_train, transcription_validate, transcription_test, translation_train, translation_validate, translation_test

def main(args):
    np.random.seed(42) # for reproduciblitity
    os.makedirs(os.path.join(args.mt_dest_file, "mt_split"), exist_ok=True)
    categories_list = os.listdir(args.jsons) # ["게임_ca3", "교육_ca5", ...] , args.jsons = "/home/ubuntu/한국어_영어/'라벨링 데이터'"
    categories_list = list(map(lambda x: os.path.join(args.jsons, x), categories_list))
    transcription_translation_set = []
    for category_path in categories_list:
        pairs = get_pairs(category_path, ratio = args.ratio)
        transcription_translation_set = [*transcription_translation_set, *pairs]   
    np.random.shuffle(transcription_translation_set)    
    transcriptions = list(map(lambda x:x[0], transcription_translation_set))
    translations = list(map(lambda x:x[1], transcription_translation_set))
    transcription_train, transcription_validate, transcription_test = np.split(
        transcriptions, [int(len(transcriptions)*0.8), int(len(transcriptions)*0.9)])
    translation_train, translation_validate, translation_test = np.split(translations, [
                                                                         int(len(translations)*0.8), int(len(translations)*0.9)])
    assert len(transcription_train) == len(
        translation_train), "train split 길이 안맞음."
    assert len(transcription_test) == len(
        translation_test), "test split 길이 안맞음."
    assert len(transcription_validate) == len(
        translation_validate), "validate split 길이 안맞음."
    transcription_train, transcription_validate, transcription_test, translation_train, translation_validate, translation_test = split_data(transcription_translation_set)
    
    with open(f"{os.path.join(args.mt_dest_file, 'mt_split', 'train.tsv')}", "a+", encoding="utf-8") as mt_train, \
            open(f"{os.path.join(args.mt_dest_file, 'mt_split','test.tsv')}", "a+", encoding="utf-8") as mt_test, \
            open(f"{os.path.join(args.mt_dest_file, 'mt_split','validation.tsv')}", "a+", encoding="utf-8") as mt_validate:
        for i in range(len(transcription_train)-1):
            mt_train.write( 
                f"{transcription_train[i]} :: {translation_train[i]}\n")
        for i in range(len(transcription_test)-1):
            mt_test.write(
                f"{transcription_test[i]} :: {translation_test[i]}\n")
        for i in range(len(transcription_validate)-1):
            mt_validate.write(
                f"{transcription_validate[i]} :: {translation_validate[i]}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mt_dest_file", type=str, required=True,
                        help="folder that will contain all the data for mt model")
    parser.add_argument("--jsons", type=str, required=True,
                        help="folder path that has json files inside of it")
    parser.add_argument("--ratio", type=float, help="ratio of the data to make splits defaults to 1", default = 1.0)
    args = parser.parse_args()
    main(args)

# script run example in bash.
# python prepare_from_json.py --asr_dest_file "./asr_train/" \
# --mt_dest_file "./mt_train/" \
# --jsons "./sample_file.json"
