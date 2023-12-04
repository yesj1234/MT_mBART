#! /usr/bin/env bash 

export PREPARE_DATA=./prepare_data.py
export TSV_TO_JSON=./tsv_to_json.py
export REFINE_DATA=./refine_data.py
export SOURCE_LANG=ko
export TARGET_LANG=en
export SPLITS_DIR=/home/ubuntu/data/mt_split

python3 $PREPARE_DATA \
--mt_dest_file /home/ubuntu/data \
--jsons /home/ubuntu/data/ \
--ratio 1

python3 $REFINE_DATA \
--tsv_splits_dir $SPLITS_DIR \
--langs "${SOURCE_LANG}_${TARGET_LANG}"

python3 $TSV_TO_JSON \
--split_path $SPLITS_DIR \
--source_lang $SOURCE_LANG \
--target_lang $TARGET_LANG