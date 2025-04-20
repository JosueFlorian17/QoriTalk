# 1) Imagen base con PyTorch + CUDA
FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel

# 2) Usuario root
USER root

# 3) Configuración de entorno
ARG DEBIAN_FRONTEND=noninteractive
ENV SHELL=/bin/bash

# 4) Información del contenedor
LABEL maintainer="TuNombre <josueflorian12317@gmail.com>"
LABEL description="Spanish-F5 (fine-tuned F5-TTS with Peruvian accent)"

# 5) Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget curl man git less openssl libssl-dev unzip unar build-essential \
    aria2 tmux vim \
    sox libsox-fmt-all libsox-fmt-mp3 libsndfile1-dev ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 6) Crear directorio de trabajo
WORKDIR /workspace

# 7) Clonar el repositorio directamente desde GitHub
RUN git clone https://github.com/JosueFlorian17/QoriTalk.git

# 8) Establecer el directorio del proyecto clonado
WORKDIR /workspace/QoriTalk
COPY model_1200000.safetensors /workspace/QoriTalk/

# 9) Instalar dependencias de Python
RUN pip install --upgrade pip

# 10) Comando por defecto
CMD ["/bin/bash"]
