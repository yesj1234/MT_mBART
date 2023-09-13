FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel

WORKDIR /home

COPY . .

RUN python -m pip install --upgrade pip 
RUN python -m pip install transformers 
RUN python -m pip install datasets 
RUN python -m pip install torch 
RUN python -m pip install torchaudio 
RUN python -m pip install numpy 
RUN python -m pip install evaluate 
RUN python -m pip install fairseq
RUN python -m pip install accelerate
RUN python -m pip install urllib3 
RUN python -m pip install requests
RUN python -m pip install sentencepiece 
RUN python -m pip install sacrebleu
RUN python -m pip install protobuf 