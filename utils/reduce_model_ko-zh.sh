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
export TARGET_LANG=zh

python $PREPARE_FROM_JSON_MT \
--mt_dest_file /home/data \
--jsons /home/data/

python $CORPUS_GEN_FOR_MBART \
--splits $SPLITS_DIR \
--source_lang $SOURCE_LANG \
--target_lang $TARGET_LANG

python $SPM_ENCODE \
--model /home/utils/sentence.bpe.model \
--inputs $SPLITS_DIR/train.ko $SPLITS_DIR/train.zh $SPLITS_DIR/test.ko $SPLITS_DIR/test.zh $SPLITS_DIR/validation.ko $SPLITS_DIR/validation.zh \
--outputs $SPLITS_DIR/train.spm.ko $SPLITS_DIR/train.spm.zh $SPLITS_DIR/test.spm.ko $SPLITS_DIR/test.spm.zh $SPLITS_DIR/validation.spm.ko $SPLITS_DIR/validation.spm.zh

python $BUILD_VOCAB \
--corpus-data "$SPLITS_DIR/*.spm.*" \
--langs ar_AR,cs_CZ,de_DE,en_XX,es_XX,et_EE,fi_FI,fr_XX,gu_IN,hi_IN,it_IT,ja_XX,kk_KZ,ko_KR,lt_LT,lv_LV,my_MM,ne_NP,nl_XX,ro_RO,ru_RU,si_LK,tr_TR,vi_VN,zh_CN \
--output /home/scripts/ft/dict.txt

python $PRUNE_MODEL \
--pre-dict /home/utils/dict.txt \
--ft-dict /home/scripts/ft/dict.txt \
--langs ar_AR,cs_CZ,de_DE,en_XX,es_XX,et_EE,fi_FI,fr_XX,gu_IN,hi_IN,it_IT,ja_XX,kk_KZ,ko_KR,lt_LT,lv_LV,my_MM,ne_NP,nl_XX,ro_RO,ru_RU,si_LK,tr_TR,vi_VN,zh_CN \
--output /home/scripts/reduced_model

python $TSV_TO_JSON \
--split_path $SPLITS_DIR \
--source_lang $SOURCE_LANG \
--target_lang $TARGET_LANG