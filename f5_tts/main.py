from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
import datetime
import os
from pathlib import Path
from f5_tts.model import DiT
from f5_tts.infer.utils_infer import (
    load_vocoder,
    load_model,
    preprocess_ref_audio_text,
    infer_process
)
from f5_tts.peruvian_voice_samples.transcribe import get_transcription
import torch
import soundfile as sf
import numpy as np

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CKPT_FILE = os.path.join(BASE_DIR, "model_1200000.safetensors")
VOCAB_FILE = os.path.join(BASE_DIR, "infer", "examples", "vocab.txt")  
REF_AUDIO = os.path.join(BASE_DIR, "peruvian_voice_samples", "ref_audio_voice_8.wav")
TRANSCRIPT_FILE = os.path.join(BASE_DIR, "peruvian_voice_samples", "transcriptions.txt")

REF_TEXT = get_transcription(REF_AUDIO, TRANSCRIPT_FILE)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Cargar modelo y vocoder una vez
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
ref_audio, ref_text = preprocess_ref_audio_text(REF_AUDIO, REF_TEXT)

def generate_audio(gen_text: str, output_path: str):
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
async def speak(text: str = Form(...)):
    now = datetime.datetime.now()
    miliseconds = now.microsecond // 1000
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S") + f"_{miliseconds}"
    output_filename = f"output_{timestamp}.wav"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    print(f"🔊 Generando audio para: {text}")
    generate_audio(text, output_path)

    return FileResponse(output_path, media_type="audio/wav", filename="output.wav")
