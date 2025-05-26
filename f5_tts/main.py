from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
import datetime
import os
from pathlib import Path
from model import DiT
from infer.utils_infer import (
    load_vocoder,
    load_model,
    preprocess_ref_audio_text,
    infer_process
)
from peruvian_voice_samples.transcribe import get_transcription
import torch
import soundfile as sf
import numpy as np

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CKPT_FILE = os.path.join(BASE_DIR, "model_1200000.safetensors")
VOCAB_FILE = os.path.join(BASE_DIR, "infer", "examples", "vocab.txt")  

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print("Cargando modelo y vocoder...")
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

def generate_audio(gen_text: str, ref_audio_path: str, ref_text: str, output_path: str):
    ref_audio, _ = preprocess_ref_audio_text(ref_audio_path, ref_text)
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

@app.post("/speak")
async def speak(text: str = Form(...), voice_type: int = Form(...)):
    if voice_type < 1 or voice_type > 8:
        return {"error": "voice_type must be between 1 and 8"}
    
    ref_audio_filename = f"ref_audio_voice_{voice_type}.wav"
    ref_audio_path = os.path.join(BASE_DIR, "peruvian_voice_samples", ref_audio_filename)
    transcript_path = os.path.join(BASE_DIR, "peruvian_voice_samples", "transcriptions.txt")
    ref_text = get_transcription(ref_audio_path, transcript_path)

    now = datetime.datetime.now()
    miliseconds = now.microsecond // 1000
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S") + f"_{miliseconds}"
    output_filename = f"output_{timestamp}.wav"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    print(f"Generando audio para: {text} con voz {voice_type}")
    generate_audio(text, ref_audio_path, ref_text, output_path)

    return FileResponse(output_path, media_type="audio/wav", filename="output.wav")
