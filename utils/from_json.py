import os 
import sys 
import logging 
import argparse 
import json 
import re
class FromJson: 
    def __init__(self, args):
        self.args = args
        self.logger = logging.getLogger("jsonReader_logger")
        self.logger.setLevel(logging.INFO)
        streamHandler = logging.StreamHandler()
        self.logger.addHandler(streamHandler)

    def gen_row(self, json_file): 
        json_data = json.load(json_file)
        
        transcription = json_data["tc_text"]
        transcription = re.sub("\n", " ", transcription)
        
        translation = json_data["tl_trans_text"]
        translation = re.sub("\n", " ", translation)
        return transcription, translation
    
    
    def main(self): 
        rows = []
        for _root, _dirs, _files in os.walk(self.args.jsons): 
            if _files: 
                for file in _files: 
                    _fname, ext = os.path.splitext(file)
                    if ext == ".json":
                        with open(os.path.join(_root, file), "r", encoding = "utf-8") as cur_json:
                            path, transcription = self.gen_row(cur_json)  
                            rows.append((path, transcription))
        # check if the dest folder exists 
        _dest_folder = self.args.dest.split("/")[:-1]
        _dest_folder = "/".join(_dest_folder)
        if not os.path.exists(_dest_folder):
            os.makedirs(os.path.join(_dest_folder))
        with open(f"{self.args.dest}", "w+", encoding="utf-8") as cur_tsv:
            for row in rows:
                cur_tsv.write(f"{row[0]} :: {row[1]}\n") 

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsons", required=True, help="path containing json files. 1 of the following. 1.Training/ 2.Validation/ 3.Test/")
    parser.add_argument("--dest", required=True, help="destination path of the generated tsv files")
    args = parser.parse_args()
    
    fromJson = FromJson(args)
    fromJson.main()