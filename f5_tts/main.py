from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
import datetime
import os
from pathlib import Path
import torch
import soundfile as sf
import numpy as np
import requests
from tqdm import tqdm
import traceback

from model import DiT
from infer.utils_infer import (
    load_vocoder,
    load_model,
    preprocess_ref_audio_text,
    infer_process
)
from peruvian_voice_samples.transcribe import get_transcription

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CKPT_FILE = os.path.join(BASE_DIR, "model_1200000.safetensors")
VOCAB_FILE = os.path.join(BASE_DIR, "infer", "examples", "vocab.txt")
CKPT_URL = "https://huggingface.co/jpgallegoar/F5-Spanish/resolve/main/model_1200000.safetensors"

# 🔽 Descarga el modelo si no está presente
def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total = int(response.headers.get('content-length', 0))
    
    with open(dest_path, 'wb') as file, tqdm(
        desc=f"Descargando {os.path.basename(dest_path)}",
        total=total,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))

if not os.path.exists(CKPT_FILE):
    print(f"🔄 Modelo no encontrado. Descargando a: {CKPT_FILE}")
    download_file(CKPT_URL, CKPT_FILE)
else:
    print(f"✅ Modelo ya existe en: {CKPT_FILE}")

# 🔧 Preparación de modelo y vocoder
print("⚙️ Cargando modelo y vocoder...")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
F5TTS_model_cfg = dict(dim=1024, depth=22, heads=16, ff_mult=2, text_dim=512, conv_layers=4)

model = load_model(
    model_cls=DiT,
    model_cfg=F5TTS_model_cfg,
    ckpt_path=CKPT_FILE,
    mel_spec_type="vocos",
    vocab_file=VOCAB_FILE,
    ode_method="euler",
    use_ema=True,
    device=DEVICE,
).to(DEVICE, dtype=torch.float32)

vocoder = load_vocoder()

# 🎵 Generar audio
def generate_audio(gen_text: str, voice_number: int, output_path: str):
    ref_audio_path = os.path.join(BASE_DIR, "peruvian_voice_samples", f"ref_audio_voice_{voice_number}.wav")
    transcript_file = os.path.join(BASE_DIR, "peruvian_voice_samples", "transcriptions.txt")

    if not os.path.exists(ref_audio_path):
        raise FileNotFoundError(f"Referencia de voz no encontrada: {ref_audio_path}")

    ref_text = get_transcription(ref_audio_path, transcript_file)
    ref_audio, ref_text = preprocess_ref_audio_text(ref_audio_path, ref_text)

    audio_chunk, final_sample_rate, _ = infer_process(
        ref_audio,
        ref_text,
        gen_text,
        model,
        vocoder,
        cross_fade_duration=0.15,
        speed=1.0
    )
    sf.write(output_path, np.array(audio_chunk), final_sample_rate)

# 📣 Endpoint de síntesis con selección de voz
@app.post("/speak")
async def speak(
    text: str = Form(...),
    voice_number: int = Form(1)  # valor predeterminado: voz 1
):
    try:
        if voice_number < 1 or voice_number > 8:
            return JSONResponse(status_code=400, content={"error": "voice_number debe estar entre 1 y 8."})

        now = datetime.datetime.now()
        miliseconds = now.microsecond // 1000
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S") + f"_{miliseconds}"
        output_filename = f"output_{timestamp}.wav"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        print(f"🔊 Generando audio para: \"{text}\" usando voz #{voice_number}")
        generate_audio(text, voice_number, output_path)

        return FileResponse(output_path, media_type="audio/wav", filename="output.wav")
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
