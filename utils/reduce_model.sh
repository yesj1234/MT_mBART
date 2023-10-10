#! /usr/bin/env bash 

export PREPARE_FROM_JSON_MT=/home/ubuntu/MT_mBART/utils/1.prepare_from_json_mt.py
export TSV_TO_JSON=/home/ubuntu/MT_mBART/utils/2.tsv_to_json.py
export SOURCE_LANG=ko
export TARGET_LANG=zh

python3 $PREPARE_FROM_JSON_MT \
--mt_dest_file /home/ubuntu/data \
--jsons /home/ubuntu/data/

python3 $TSV_TO_JSON \
--split_path $SPLITS_DIR \
--source_lang $SOURCE_LANG \
--target_lang $TARGET_LANG