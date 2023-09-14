#! /usr/bin/bash 

sudo docker run -it --ipc host --gpus all -v /home/ubuntu/data:/home/data -v /home/ubuntu/MT_mBART/scripts:/home/scripts mbart bash

