#! /usr/bin/env bash 

export PREPARE_FROM_JSON_MT=/home/ubuntu/MT_mBART/utils/1.prepare_from_json_mt.py
export TSV_TO_JSON=/home/ubuntu/MT_mBART/utils/2.tsv_to_json.py
export REFINE_DATA=/home/ubuntu/MT_mBART/utils/refine_data.py
export SOURCE_LANG=ko
export TARGET_LANG=en
export SPLITS_DIR=/home/ubuntu/중간_한국어_중국어/mt_split

python3 $PREPARE_FROM_JSON_MT \
--mt_dest_file /home/ubuntu/중간_한국어_중국어 \
--jsons /home/ubuntu/중간_한국어_중국어/

python3 $REFINE_DATA \
--tsv_splits_dir /home/ubuntu/중간_한국어_중국어/mt_split \
--langs ko-zh

python3 $TSV_TO_JSON \
--split_path $SPLITS_DIR \
--source_lang $SOURCE_LANG \
--target_lang $TARGET_LANG