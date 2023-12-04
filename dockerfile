FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel

WORKDIR /home

COPY . .
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
RUN apt-get update && apt-get install -y locales
RUN locale-gen ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8
RUN apt-get install -y wget sudo 

RUN python -m pip install --upgrade pip 
RUN python -m pip install transformers 
RUN python -m pip install datasets 
RUN python -m pip install torch 
RUN python -m pip install torchaudio 
RUN python -m pip install torchvision
RUN python -m pip install numpy 
RUN python -m pip install evaluate 
RUN python -m pip install fairseq
RUN python -m pip install accelerate
RUN python -m pip install urllib3 
RUN python -m pip install requests
RUN python -m pip install sentencepiece 
RUN python -m pip install sacrebleu
RUN python -m pip install sacrebleu[ja]
RUN python -m pip install sacrebleu[ko]
RUN python -m pip install protobuf 