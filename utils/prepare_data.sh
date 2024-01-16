#! /usr/bin/env bash 

export FROM_JSON=./from_json.py
export TSV_TO_JSON=./tsv_to_json.py
export REFINE_DATA=./refine_data.py
export SOURCE_LANG=en
export TARGET_LANG=ko
export SPLITS_DIR=/home/ubuntu/mt_split

python3 from_json.py --jsons /home/ubuntu/1.Training/2.영어/ --dest ${SPLITS_DIR}/train.tsv 
python3 from_json.py --jsons /home/ubuntu/2.Validation/2.영어/ --dest ${SPLITS_DIR}/validation.tsv 
python3 from_json.py --jsons /home/ubuntu/3.Test/2.영어/ --dest ${SPLITS_DIR}/test.tsv 

python3 $REFINE_DATA \
--tsv_splits_dir $SPLITS_DIR \
--langs "${SOURCE_LANG}_${TARGET_LANG}"

python3 $TSV_TO_JSON \
--split_path $SPLITS_DIR \
--source_lang $SOURCE_LANG \
--target_lang $TARGET_LANG
