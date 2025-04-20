import os

def load_transcriptions(transcript_file):
    transcriptions = {}
    with open(transcript_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                parts = line.split(".- ")  # Split at ".- "
                if len(parts) == 2:
                    key = parts[0].strip()  # Extract the number (e.g., "1", "2", etc.)
                    text = parts[1].strip()  # Extract the actual transcription text
                    transcriptions[key] = text
    return transcriptions

def get_transcription(ref_audio, transcript_file):
    # Extract the audio file number
    audio_basename = os.path.basename(ref_audio)  # Get only the filename
    audio_number = audio_basename.split("_")[-1].split(".")[0]  # Extract the number (e.g., "1", "2", etc.)

    # Load transcriptions
    transcriptions = load_transcriptions(transcript_file)

    # Return the corresponding transcription or a default message
    return transcriptions.get(audio_number, "Transcription not found.")
