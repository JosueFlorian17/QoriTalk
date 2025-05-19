FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel

LABEL maintainer="Josue Florian <josueflorian12317@gmail.com>"
LABEL description="QoriTalk: Spanish-F5 TTS con acento peruano"

ENV DEBIAN_FRONTEND=noninteractive
ENV SHELL=/bin/bash
WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl git vim tmux man less openssl libssl-dev \
    unzip unar build-essential aria2 \
    sox libsox-fmt-all libsox-fmt-mp3 libsndfile1-dev ffmpeg \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/JosueFlorian17/QoriTalk.git

WORKDIR /workspace/QoriTalk

RUN pip install --upgrade pip && \
    pip install \
        torch torchaudio \
        transformers gradio soundfile numpy librosa scipy \
        tqdm click cached_path safetensors pydub vocos \
        jieba pypinyin x-transformers datasets wandb accelerate \
        ema-pytorch thop sentencepiece torchdiffeq matplotlib requests \
        fastapi uvicorn

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
