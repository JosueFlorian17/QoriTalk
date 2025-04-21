import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '')))
import requests
from tqdm import tqdm
import torch
import torchaudio
import soundfile as sf
import numpy as np
import datetime
from model import DiT
from infer.utils_infer import (
    load_vocoder,
    load_model,
    preprocess_ref_audio_text,
    infer_process
)
from peruvian_voice_samples.transcribe import get_transcription



BASE_DIR = os.path.dirname(os.path.abspath(__file__))



CKPT_FILE = os.path.join(BASE_DIR, "model_1200000.safetensors")
VOCAB_FILE = os.path.join(BASE_DIR,  "infer", "examples", "vocab.txt")  
REF_AUDIO = os.path.join(BASE_DIR, "peruvian_voice_samples", "ref_audio_voice_8.wav")
TRANSCRIPT_FILE = os.path.join(BASE_DIR, "peruvian_voice_samples", "transcriptions.txt")
CKPT_URL = "https://huggingface.co/jpgallegoar/F5-Spanish/resolve/main/model_1200000.safetensors"

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
    print(f"Modelo no encontrado. Descargando a: {CKPT_FILE}")
    download_file(CKPT_URL, CKPT_FILE)
else:
    print(f"Modelo ya existe en: {CKPT_FILE}")

now = datetime.datetime.now()
miliseconds = now.microsecond // 1000
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S") + f"_{miliseconds}"

REF_TEXT = get_transcription(REF_AUDIO, TRANSCRIPT_FILE)
print(REF_TEXT)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


print("Cargando el modelo...")
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


print("Cargando el vocoder...")
vocoder = load_vocoder()


print("Procesando referencia de audio...")
ref_audio, ref_text = preprocess_ref_audio_text(REF_AUDIO, REF_TEXT)
audio, sr = torchaudio.load(ref_audio)
output_path = os.path.join(BASE_DIR, "outputs", f"output_{timestamp}.wav")



def generate_audio(gen_text, output_path):
    """
    Genera un archivo de audio a partir del texto ingresado.
    
    :param gen_text: Texto a convertir en audio.
    :param output_path: Ruta donde se guardará el archivo de salida.
    """
    print("Generando el audio...")
    
    # Realizar inferencia
    audio_chunk, final_sample_rate, _ = infer_process(
        ref_audio,
        ref_text,
        gen_text,
        model,
        vocoder,
        cross_fade_duration=0.15,
        speed=1.0
    )

    # Guardar el audio generado
    sf.write(output_path, np.array(audio_chunk), final_sample_rate)
    print(f"✅ Audio generado y guardado en: {output_path}")

# --- USO DEL SCRIPT ---
if __name__ == "__main__":
    status= True
    while status:
        now = datetime.datetime.now()
        miliseconds = now.microsecond // 1000
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S") + f"_{miliseconds}"
        texto = input("Ingresa el texto a convertir en audio: ")
        output_path = os.path.join(BASE_DIR, "outputs", f"output_{timestamp}.wav")
        generate_audio(texto, output_path)
        status = input("¿Desea generar otro audio? (s/n): ").lower() == "s"

