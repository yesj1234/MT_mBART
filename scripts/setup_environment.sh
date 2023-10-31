# # 1. install gcc and cmake
sudo apt install -y gcc
sudo apt install -y cmake

# # 2. install cuda
wget wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update 
sudo apt-get install -y cuda

# # 3. install pip
sudo apt install -y python3-pip 

# 4. install python libraries 
pip install transformers datasets torch torchaudio torchvision numpy jiwer soundfile librosa evaluate
pip install accelerate -U
pip install --upgrade urllib3 requests
pip install sentencepiece sacrebleu "sacrebleu[ja]" "sacrebleu[ko]"
pip install -U protobuf
pip install wandb
