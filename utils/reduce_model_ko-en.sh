#! /usr/bin/env bash 

# prepare reduce model for mbart
export PREPARE_FROM_JSON_MT=/home/utils/1.prepare_from_json_mt.py
export TSV_TO_JSON=/home/utils/2.tsv_to_json.py
export CORPUS_GEN_FOR_MBART=/home/utils/corpus_gen_for_mbart.py
export SPM_ENCODE=/home/utils/spm_encode.py
export BUILD_VOCAB=/home/utils/build_vocab.py
export PRUNE_MODEL=/home/utils/prune_model.py
export SPLITS_DIR=/home/data/mt_split
export SOURCE_LANG=ko
export TARGET_LANG=en

python $PREPARE_FROM_JSON_MT \
--mt_dest_file /home/data \
--jsons /home/data/

python $TSV_TO_JSON \
--split_path $SPLITS_DIR \
--source_lang $SOURCE_LANG \
--target_lang $TARGET_LANG