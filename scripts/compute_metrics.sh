#! /usr/bin/env bash 

python3 compute_metrics.py \
--model_repo yesj1234/koen_mbartLarge_100p_run1 \
--data /home/ubuntu/enko_data/mt_split/test_refined.json \
--src_lang ko_KR \
--tgt_lang en_XX
