FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel

USER root

ARG DEBIAN_FRONTEND=noninteractive
ENV SHELL=/bin/bash

LABEL maintainer="TuNombre <josueflorian12317@gmail.com>"
LABEL description="Spanish-F5 (fine-tuned F5-TTS with Peruvian accent)"

RUN apt-get update && apt-get install -y \
    wget curl man git less openssl libssl-dev unzip unar build-essential \
    aria2 tmux vim \
    sox libsox-fmt-all libsox-fmt-mp3 libsndfile1-dev ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /workspace

RUN git clone https://github.com/JosueFlorian17/QoriTalk.git

WORKDIR /workspace/QoriTalk
COPY model_1200000.safetensors /workspace/QoriTalk/

RUN pip install --upgrade pip && \
    pip install torch torchaudio transformers gradio soundfile numpy librosa scipy tqdm click \
    cached_path safetensors pydub vocos jieba pypinyin x-transformers datasets wandb accelerate \
    ema-pytorch thop sentencepiece torchdiffeq matplotlib requests tqdm

CMD ["/bin/bash"]
