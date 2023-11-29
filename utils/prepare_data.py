import json
import os
import argparse
from sys import platform
import numpy as np
import re
import logging

class DataSplitter:
    def __init__(self, args):
        self.args = args
        self.logger = logging.getLogger("splitting_logger")
        self.logger.setLevel(logging.INFO)
        self.streamHandler = logging.StreamHandler()
        self.logger.addHandler(streamHandler)
        
    def _get_necessary_info(self, json_file):
        json_data = json.load(json_file)
        json_filename = json_data["fi_sound_filepath"].split("/")[-3:]
        json_filename = "/".join(json_filename)
        json_filename = json_filename.replace(".wav", ".json")
        
        transcription = json_data["tc_text"]
        transcription = re.sub("\n", " ", transcription)
        
        translation = json_data["tl_trans_text"]
        translation = re.sub("\n", " ", translation)
        return transcription, translation, json_filename

    def _get_pairs(self, dir_path, ratio = 1.0):
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
                                        transcription, translation, json_filename = get_neccesary_info(
                                            json_file)
                                        pairs.append((transcription, translation, json_filename))
                                    except Exception as e:
                                        logger.warning(e)
                                        logger.warning(file)
        np.random.shuffle(pairs) # shuffle in-place and return none.
        maximum_index = int(len(pairs) * ratio)
        return pairs[:maximum_index] # return the given ratio. defaults to 100%. 

    def _split_data(self, pairs):
        transcriptions = list(map(lambda x:x[0], pairs))
        translations = list(map(lambda x:x[1], pairs))
        json_filenames = list(map(lambda x:x[2], pairs))
        
        transcription_train, transcription_validate, transcription_test = np.split(
            transcriptions, [int(len(transcriptions)*0.8), int(len(transcriptions)*0.9)])
        translation_train, translation_validate, translation_test = np.split(translations, [
                                                                            int(len(translations)*0.8), int(len(translations)*0.9)])
        json_filenames_train, json_filenames_validate, json_filenames_test = np.split(json_filenames, [
                                                                            int(len(json_filenames)*0.8), int(len(json_filenames)*0.9)])


        assert len(transcription_train) == len(
            translation_train), "train split 길이 안맞음."
        assert len(transcription_test) == len(
            translation_test), "test split 길이 안맞음."
        assert len(transcription_validate) == len(
            translation_validate), "validate split 길이 안맞음."
        return transcription_train, transcription_validate, transcription_test, translation_train, translation_validate, translation_test, json_filenames_train, json_filenames_validate, json_filenames_test

    def _write_split_tsv(self, destination, transcriptions, translations):
        assert isinstance(transcriptions, np.ndarray) == True, "transcriptions should be a np.ndarray"
        assert isinstance(translations, np.ndarray) == True, "translations should be a np.ndarray"    

        split_fname, ext = os.path.splitext(destination)
        split_fname = split_fname.split("/")[-1]
        logger.info(f"""
                    writing {split_fname + ext} in {destination}. 
                    transcription length: {len(transcriptions)}
                    translation length  : {len(translations)}""")
        with open(destination, "a+", encoding = "utf-8") as split:
            for i in range(len(transcriptions)-1):
                split.write(f"{transcriptions[i]} :: {translations[i]}\n")
            
    def _write_filename_tsv(self, destination, filenames, transcriptions, translations):
        assert isinstance(transcriptions, np.ndarray) == True, "transcriptions should be a np.ndarray"
        assert isinstance(translations, np.ndarray) == True, "translations should be a np.ndarray"    
        assert isinstance(filenames, np.ndarray) == True, "filenames should be a np.ndarray"
        
        split_fname, ext = os.path.splitext(destination)
        split_fname = split_fname.split("/")[-1]
        logger.info(f"""
                    writing {split_fname + ext} in {destination}. 
                    transcription length: {len(transcriptions)} 
                    translation length  : {len(translations)}""")
        with open(destination, "a+", encoding = "utf-8") as split:
            for i in range(len(transcriptions)-1):
                split.write(f"{filenames[i]} :: {transcriptions[i]} :: {translations[i]}\n") 
    
    def split_data(args):
        np.random.seed(42) # for reproduciblitity
        os.makedirs(os.path.join(args.mt_dest_file, "mt_split"), exist_ok=True)
        categories_list = os.listdir(args.jsons) # ["게임_ca3", "교육_ca5", ...] , args.jsons = "/home/ubuntu/한국어_영어/'라벨링 데이터'"
        categories_list = list(map(lambda x: os.path.join(args.jsons, x), categories_list))
        transcription_translation_set = []
        for category_path in categories_list:
            pairs = get_pairs(category_path, ratio = args.ratio)
            transcription_translation_set = [*transcription_translation_set, *pairs]   
        np.random.shuffle(transcription_translation_set)    
        transcription_train, transcription_validation, transcription_test, \
        translation_train, translation_validation, translation_test, \
        json_filenames_train, json_filenames_validation, json_filenames_test = split_data(transcription_translation_set)

        split_args = {
            "split_tsv_args": [("train.tsv", transcription_train, translation_train),
                            ("validation.tsv", transcription_validation, translation_validation),
                            ("test.tsv", transcription_test, translation_test)],
            "filename_tsv_args": [("filename_train.tsv", json_filenames_train, transcription_train, translation_train),
                                ("filename_validation.tsv", json_filenames_validation, transcription_validation, translation_validation),
                                ("filename_test.tsv", json_filenames_test, transcription_test, translation_test)]
        }
        
        for args_tuple in split_args["split_tsv_args"]:
            dest, transcription_list, translation_list = args_tuple
            assert isinstance(dest, str) == True, "dest should be type of string."
            write_split_tsv(destination = os.path.join(args.mt_dest_file, "mt_split", dest),
                            transcriptions = transcription_list,
                            translations=translation_list)
        
        for args_tuple in split_args["filename_tsv_args"]:
            dest, filename_list, transcription_list, translation_list = args_tuple
            assert isinstance(dest, str) == True, "dest should be type of string."
            write_filename_tsv(destination = os.path.join(args.mt_dest_file, "mt_split", dest),
                                filenames= filename_list,
                                transcriptions = transcription_list,
                                translations=translation_list)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mt_dest_file", type=str, required=True,
                        help="folder that will contain all the data for mt model")
    parser.add_argument("--jsons", type=str, required=True,
                        help="folder path that has json files inside of it")
    parser.add_argument("--ratio", type=float, help="ratio of the data to make splits defaults to 1", default = 1.0)
    args = parser.parse_args()
    
    data_splitter = DataSplitter(args)
    data_splitter.split_data()