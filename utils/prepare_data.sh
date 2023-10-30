#! /usr/bin/env bash 

export PREPARE_FROM_JSON_MT=/home/ubuntu/MT_mBART/utils/prepare_from_json_mt.py
export TSV_TO_JSON=/home/ubuntu/MT_mBART/utils/tsv_to_json.py
export REFINE_DATA=/home/ubuntu/MT_mBART/utils/refine_data.py
export SOURCE_LANG=en
export TARGET_LANG=ko
export SPLITS_DIR=/home/ubuntu/영한/mt_split

python3 $PREPARE_FROM_JSON_MT \
--mt_dest_file /home/ubuntu/영한 \
--jsons /home/ubuntu/영한/ \
--ratio 1

python3 $REFINE_DATA \
--tsv_splits_dir /home/ubuntu/영한/mt_split \
--langs "${SOURCE_LANG}_${TARGET_LANG}"

python3 $TSV_TO_JSON \
--split_path $SPLITS_DIR \
--source_lang $SOURCE_LANG \
--target_lang $TARGET_LANG