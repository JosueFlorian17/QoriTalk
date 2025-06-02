# QoriTalk
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow)

> QoriTalk es un sistema **Text-to-Speech (TTS)** que genera voces realistas en **español peruano**, incluyendo acentos regionales.

“Qori” significa “oro” en quechua. Este proyecto busca dar voz de oro a los acentos y lenguas del Perú.
---

## ✨ Características

| Característica                  | Descripción                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| 🗣️ Voces regionales peruanas  | Soporte para acentos Peruanos                                                |
| 👨‍👩‍👧‍👦 Géneros soportados       | Masculino y femenino                                                       |
| 🎛️ Personalización            | Control de velocidad, tono y estilo de voz (en versiones futuras)          |
| ⚡ Inferencia optimizada       | Soporte para GPU y CPU                                                     |
| 🔊 Ejemplos de voz             | Audios realistas entrenados con datos curados                              |

---

## 📥 Instalación

### Via Docker Hub
1. Descargar la imagen del contenedor desde Docker Hub:

```
docker pull osheny/qoritalk:0.0.1
```

2. Iniciar el contenedor con el puerto 8000 expuesto:
```
docker run -it -p 8000:8000 josueflorian/qoritalk:latest
```

> Mediante este comando, el usuario activa el API de Qoritalk, pudiendo realizar solicitudes de síntesis de voz con el comando CURL adjunto

No requiere un entorno virtual diferente, el contenedor recopila todos los recursos necesarios para el correcto funcionamiento de QoriTalk

### De manera local y editable
Para desarrollo o personalización, puedes instalar QoriTalk de forma editable. Primero, clona el repositorio:
```
git clone https://github.com/JosueFlorian17/QoriTalk.git
cd QoriTalk\f5_tts
```
Luego crea un entorno virtual con alguna de las siguientes opciones:

➤ Opción 1: conda (recomendado si usas Anaconda)
```
conda create -n qoritalk python=3.8
conda activate qoritalk
pip install -r requirements.txt
```

➤ Opción 2: venv (Python nativo)

```
python -m venv venv
source venv/bin/activate      # En Linux/macOS
venv\Scripts\activate.bat     # En Windows
pip install -r requirements.txt

```
Una vez esté todo listo, puedes correr
```
python tts_test_peruvian_accent.py
```
Para comenzar a generar archivos de audio y experimentar con el modelo

---
## Resultados de pruebas de Benchmarking

| Característica                  | Descripción                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
|     |                                              |
|        |                                                   |
|         |           |
|       |                                            |
|            |                            |


---
## Licencia
QoriTalk, como modelo "fine-tuned" de F5-TTS, se encuentra publicado bajo la licencia del MIT 