# MT EXAMPLE

## PREPROCESSING 산출물 DATA

0. **_validation_**

```bash
python3 0.json_validator.py --jsons /path/to/the/folder/containing/json/files
e.g.
python3 0.json_validator.py --jsons ./output
```

1. **_prepare_from_json_mt.py_**

```bash
python3 1.prepare_from_json_mt.py --mt_dest_folder /path/to/the/destination/folder --jsons /path/to/the/folder/containing/jsons
e.g.
python3 1.prepare_from_json_mt.py --mt_dest_folder ./mt_split --jsons ./output/한국어(KO)_영어(EN)

```

2. **_tsv_to_json.py_**

```bash
# preparing json file that will be used in run_training_mbart.py.
# source_lang : en ko ja zh
# target_lang : en ko ja zh
python3 2.tsv_to_json.py --split_path /path/to/the/folder/containing/splits.tsv --source_lang source_lang --target_lang target_lang
e.g.
python3 2.tsv_to_json.py --split_path ./mt_split --source_lang ko --target_lang en
```

3. **_preparing the data for model pruning_**. [tackling OOM issue while training with GPU](https://github.com/facebookresearch/fairseq/issues/2120)

   download the base model mbart.cc25.v2. the folder contains model.pt, dict.txt, sentence.bpe.model

   ```
   wget https://dl.fbaipublicfiles.com/fairseq/models/mbart/mbart.cc25.v2.tar.gz
   tar -xzvf mbart.CC25.tar.gz
   ```

   **FIRST**, generate corpus data for mbart.  
   FROM train.tsv TO train.ko train.en  
   FROM test.tsv TO test.ko test.en  
   FROM validation.tsv TO validation.ko validation.en

   ```bash
   # the script is in mt_example/utils
   python3 corpus_gen_for_mbart.py --splits /path/to/the/folder/containing/splits --source_lang source_lang --target_lang target_lang
   e.g.
   python3 corpus_gen_for_mbart.py --splits ./mt_split --source_lang ko --target_lang en
   ```

   **SECOND**, encode the generated corpus with sentencepiece

   FROM train.ko train.en TO train.spm.ko train.spm.en  
   FROM test.ko test.en TO test.spm.ko test.spm.en  
   FROM validatioin.ko validatioin.en TO validatioin.spm.ko validatioin.spm.en  
   BEAWARE that the length of inputs and outputs must match.

   ```bash
   # the script is in mt_example/utils as well
   python3 spm_encode.py --model /path/to/the/saved/model --inputs /path/to/train.ko /path/to/train.en --outputs /path/to/train.spm.ko /path/to/train.spm.en --min_length 10 --max_length 512
   e.g.
   export SPLITS_DIR=/home/ubuntu/contents/한국어_영어
   python3 spm_encode.py --model ./sentence.bpe.model --inputs $SPLITS_DIR/train.ko $SPLITS_DIR/train.en $SPLITS_DIR/test.ko $SPLITS_DIR/test.en $SPLITS_DIR/validation.ko $SPLITS_DIR/validation.en --outputs $SPLITS_DIR/train.spm.ko $SPLITS_DIR/train.spm.en $SPLITS_DIR/test.spm.ko $SPLITS_DIR/test.spm.en $SPLITS_DIR/validation.spm.ko $SPLITS_DIR/validation.spm.en
   export SPLITS_DIR=/home/ubuntu/contents/한국어_일본어
   python3 spm_encode.py --model ./sentence.bpe.model --inputs $SPLITS_DIR/train.ko $SPLITS_DIR/train.ja $SPLITS_DIR/test.ko $SPLITS_DIR/test.ja $SPLITS_DIR/validation.ko $SPLITS_DIR/validation.ja --outputs $SPLITS_DIR/train.spm.ko $SPLITS_DIR/train.spm.ja $SPLITS_DIR/test.spm.ko $SPLITS_DIR/test.spm.ja $SPLITS_DIR/validation.spm.ko $SPLITS_DIR/validation.spm.ja
   export SPLITS_DIR=/home/ubuntu/contents/한국어_중국어
   python3 spm_encode.py --model ./sentence.bpe.model --inputs $SPLITS_DIR/train.ko $SPLITS_DIR/train.zh $SPLITS_DIR/test.ko $SPLITS_DIR/test.zh $SPLITS_DIR/validation.ko $SPLITS_DIR/validation.zh --outputs $SPLITS_DIR/train.spm.ko $SPLITS_DIR/train.spm.zh $SPLITS_DIR/test.spm.ko $SPLITS_DIR/test.spm.zh $SPLITS_DIR/validation.spm.ko $SPLITS_DIR/validation.spm.zh

   ```

   **THIRD**, build the vocab.txt from encoded spm splits (e.g. train.spm.ko train.spm.en)  
   --langs argument is fixed argument with "ar_AR,cs_CZ,de_DE,en_XX,es_XX,et_EE,fi_FI,fr_XX,gu_IN,hi_IN,it_IT,ja_XX,kk_KZ,ko_KR,lt_LT,lv_LV,my_MM,ne_NP,nl_XX,ro_RO,ru_RU,si_LK,tr_TR,vi_VN,zh_CN"  
   generated file will be saved as one dict.txt file

   ```bash
   python3 build.py --corpus-data "/path/to/spm_splits_with_regex" --langs ar_AR,cs_CZ,de_DE,en_XX,es_XX,et_EE,fi_FI,fr_XX,gu_IN,hi_IN,it_IT,ja_XX,kk_KZ,ko_KR,lt_LT,lv_LV,my_MM,ne_NP,nl_XX,ro_RO,ru_RU,si_LK,tr_TR,vi_VN,zh_CN --output /path/to/the/folder/dict.txt
   e.g.
   export SPLITS_DIR=/home/ubuntu/path/to/the/splits_dir
   python3 build.py --corpus-data "$SPLITS_DIR/*.spm.*" --langs ar_AR,cs_CZ,de_DE,en_XX,es_XX,et_EE,fi_FI,fr_XX,gu_IN,hi_IN,it_IT,ja_XX,kk_KZ,ko_KR,lt_LT,lv_LV,my_MM,ne_NP,nl_XX,ro_RO,ru_RU,si_LK,tr_TR,vi_VN,zh_CN --output ../ft/dict.txt
   ```

   **FORTH**, Finally prune the model with generated **_dict.txt_** file

   ```bash
   python3 prune_mbart.py --pre-dict /home/ubuntu/mbart.cc25.v2/dict.txt --ft-dict ../ft/dict.txt --langs ar_AR,cs_CZ,de_DE,en_XX,es_XX,et_EE,fi_FI,fr_XX,gu_IN,hi_IN,it_IT,ja_XX,kk_KZ,ko_KR,lt_LT,lv_LV,my_MM,ne_NP,nl_XX,ro_RO,ru_RU,si_LK,tr_TR,vi_VN,zh_CN --output ../reduced_model
   ```

   **FIFTH**, Since I'm using transformers library source code [run_translation.py](https://github.com/huggingface/transformers/blob/main/examples/pytorch/translation/run_translation.py), needs to load the correct model and configuration and tokenizer.
   the model, config, and tokenizer can be loaded as follows

   ```python
   from transformers import (
       AutoConfig,
       AutoTokenizer,
       AutoModelForSeq2SeqLM
   )
   config = AutoConfig.from_pretrained('facebook/mbart-large-cc25')
   tokenizer = AutoTokenizer.from_pretrained('facebook/mbart-large-cc25')
   model = AutoModelForSeq2SeqLM.from_pretrained(
       '/path/to/the/saved/pruned_model.pt',
       config=config)
   ```

   **LASTLY**, go for training with pruned model with right settings. settings can be changed in run_training_mbart.json

   ```bash
   # mt_example/run_training_mbart.sh
   bash run_training_mbart.sh
   ```
## Dockerizing
### Prerequisites
Docker and NVIDIA driver MUST be installed in your host OS. 
1. Add Docker's official GPG key
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```
2. Add the repository to Apt sources:
```bash
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
3. verify the Docker Engine installation is succesful by running the hello-world image
```bash
sudo docker run hello-world
```
4. install docker nvidia(NVIDIA driver MUST be installed in the host OS)
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
```
5. NVIDIA-docker install
```bash
sudo apt-get update
sudo apt-get install -y nvidia-docker2
```
6. rerun docker service
```bash
sudo systemctl restart docker
```
7. test if nvidia docker is successfully installed
```bash
sudo docker run --rm --gpus all ubuntu:20.04 nvidia-smi
```
## Simply run the training scripts in 3 steps with docker. 
1. build 
```bash
sudo docker build -t mbart .
```
2. run
```bash
bash run_container.sh
``` 
3. preprocess(inside the container)
```bash
bash reduce_model_ko-ja.sh # bash reduce_model_<source_lang>-<target_lang>.sh
```
4. and, train!
```bash
bash run_training_mbart.sh
```

# Multi gpu 환경에서 trainer api 사용하기.

1. bash로 python script 실행 하기 혹은 그냥 python 명령어 실행.

```bash
LOCAL_RANK=0,1,2,3 \
CUDA_VISIBLE_DEVICES=0,1,2,3 \
python3 -m torch.distributed.launch --nproc_per_node 4 \
--use-env run_translation.py \
run_translation_gpu_mt.json
```
# ENVIRONMENT
- OS: Canonical Ubuntu 20.04 
- CPU: 64 OCPU(Oracle CPU)
- Memory: 16GB(per GPU)
- Storage: 7.68TB NVMe SSD Storage(x2)
- GPU: NVIDIA A10(x4)