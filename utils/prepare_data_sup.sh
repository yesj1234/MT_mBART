#! /usr/bin/env bash 

export FROM_JSON=./from_json.py
export TSV_TO_JSON=./tsv_to_json.py
export REFINE_DATA=./refine_data.py
export SOURCE_LANG=ko
export TARGET_LANG=en
export SPLITS_DIR=/home/ubuntu/mt_split

python3 from_json.py --jsons /home/ubuntu/3.보완조치완료/1.Training/2.라벨링데이터/2.영어/ --dest /home/ubuntu/mt_splt/train.tsv 
python3 from_json.py --jsons /home/ubuntu/3.보완조치완료/2.Validation/2.라벨링데이터/2.영어/ --dest /home/ubuntu/mt_split/validation.tsv
python3 from_json.py --jsons /home/ubuntu/3.보완조치완료/3.Test/2.라벨링데이터/2.영어/ --dest /home/ubuntu/mt_split/test.tsv



python3 $REFINE_DATA \
--tsv_splits_dir $SPLITS_DIR \
--langs "${SOURCE_LANG}_${TARGET_LANG}"

python3 $TSV_TO_JSON \
--split_path $SPLITS_DIR \
--source_lang $SOURCE_LANG \
--target_lang $TARGET_LANG