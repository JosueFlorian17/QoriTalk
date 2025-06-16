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
docker run -it -p 8000:8000 osheny/qoritalk:0.0.1
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
## Realizando la llamada al API:
> El API de Qoritalk permite generar audios al ser llamado con un comando **curl** con el formato siguiente
```
curl -X POST http://localhost:8000/speak -H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" --data-urlencode "text=" --data-urlencode "voice_number=8" -o outputlargo.wav
```

Esto generará un archivo **output1.wav** en la carpeta desde donde se ejecute el comando, listo para reproducirse.

### Explicación de parámetros:

- **http://localhost:8000/speak**  
  Dirección local del endpoint `/speak`, habilitado al ejecutar el contenedor de QoriTalk en el puerto 8000.

- **-X POST**  
  Indica que se trata de una solicitud POST, usada para enviar datos al servidor.

- **-d "text=..."**  
  Parámetro obligatorio que define el texto que se desea convertir a audio.

- **-d "voice_number=..."**  
  Especifica qué voz usar. Por defecto puedes definir valores en el rango de 1 a 8, cada una corresponde a un tipo de voz visto en las **demostraciones**.

- **-o output1.wav**  
  Define el nombre del archivo de salida donde se guardará el audio generado por el API.

---

Puedes automatizar pruebas o integrar esta llamada fácilmente en scripts o aplicaciones externas para aprovechar QoriTalk como un motor TTS con acento peruano.


## Resultados de pruebas de Benchmarking

| Prueba                          | Frase de ejemplo                                                                                   | Audio de ejemplo                        |
|--------------------------------|--------------------------------------------------------------------------------------------------|---------------------------------------|
| Cita narrativa           | “Nada me impresiona más que los hombres que lloran. Nuestra cobardía nos ha hecho considerar el llanto como cosa de mujercitas. Cuando solo lloran los valientes” (de *Solo lloran los valientes* de **Julio ramón Ribeyro**) | [Audio](https://github.com/JosueFlorian17/QoriTalk/blob/main/voice_demonstration/voice1.wav)    |
| Precisión en frases largas   | “El gran error de la naturaleza humana es adaptarse. La verdadera felicidad está construida por un perpetuo estado de iniciación, de entusiasmo constante” (de **Julio ramón Ribeyro**)            | [Audio](https://github.com/JosueFlorian17/QoriTalk/blob/main/voice_demonstration/voice2.wav)    |
| Manejo de pausas   | “El ser, absolutamente inexpresivo no existe, es un ente de pura abstracción. Si existiera sería la negación de toda facultad estética, de toda condición humana”    (de *Trilce* de **César Vallejo**)            | [Audio](https://github.com/JosueFlorian17/QoriTalk/blob/main/voice_demonstration/voice4.wav)    |
| Frase corta | “El deber no es el éxito, es la lucha” (de *Tradiciones Peruanas* de **Ricardo Palma**)| [Audio](https://github.com/JosueFlorian17/QoriTalk/blob/main/voice_demonstration/voice6.wav)    |
| Indicaciones médicas | “Por favor, indique si siente dolor en el pecho, dificultad para respirar o mareos.”| [Audio](https://github.com/JosueFlorian17/QoriTalk/blob/main/voice_demonstration/voice7.wav)    |

---



---
## Licencia
QoriTalk, como modelo "fine-tuned" de F5-TTS, se encuentra publicado bajo la licencia del MIT 
