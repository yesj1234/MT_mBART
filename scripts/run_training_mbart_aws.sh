LOCAL_RANK=0,1,2,3,4,5,6,7 \
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
python3 -m torch.distributed.launch --nproc_per_node 8 \
--use-env run_training_mbart.py \
run_training_mbart.json
