# MT EXAMPLE

## PREPROCESSING 산출물 DATA

1. **_prepare_from_json_mt.py_**

```bash
python3 prepare_from_json_mt.py --mt_dest_folder /path/to/the/destination/folder --jsons /path/to/the/folder/containing/jsons --ratio 1
e.g.
python3 prepare_from_json_mt.py --mt_dest_folder ./mt_split --jsons ./output/한국어(KO)_영어(EN) --ratio 1

```

2. **_refine_data.py_**

```bash
python3 refine_data.py --tsv_splits_dir /home/ubuntu/한국어(KO)_영어(EN)/mt_split --langs $SOURCE_LANG_$TARGET_LANG
e.g.
python3 refine_data.py --tsv_splits_dir /home/ubuntu/한국어(KO)_영어(EN)/mt_split --langs ko_en
```

3. **_tsv_to_json.py_**

```bash
# preparing json file that will be used in run_training_mbart.py.
# source_lang : en ko ja zh
# target_lang : en ko ja zh
python3 tsv_to_json.py --split_path /path/to/the/folder/containing/splits.tsv --source_lang source_lang --target_lang target_lang
e.g.
python3 tsv_to_json.py --split_path ./mt_split --source_lang ko --target_lang en
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

## Simply run the training scripts in 4 steps with docker.

1. build

```bash
sudo docker build -t mbart . # don't change the name of the image
```

2. run

```bash
bash run_container.sh # sudo docker run -it --ipc host --gpus all -v /home/ubuntu/data:/home/data -v /home/ubuntu/MT_mBART/scripts:/home/scripts mbart bash
```

3. preprocess(inside the container)

```bash
bash prepare_data.sh
```

4. and, train!

```bash
bash run_training_mbart.sh
```

# ENVIRONMENT

- OS: Canonical Ubuntu 20.04
- CPU: 64 OCPU(Oracle CPU)
- Memory: 16GB(per GPU)
- Storage: 7.68TB NVMe SSD Storage(x2)
- GPU: NVIDIA A10(x4)
