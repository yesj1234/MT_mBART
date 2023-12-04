#! /usr/bin/env bash 

python3 generate_predictions.py \
--model_repo yesj1234/koen_mbartLarge_100p_run1 \
--data /home/ubuntu/enko_data/mt_split/test_refined.json \
--src_lang en_XX \
--tgt_lang ko_KR \
--file_name enko_generated_test_score.txt
