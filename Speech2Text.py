import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import wave
import queue
from googletrans import Translator

# Configuration
SAMPLE_RATE = 16000
CHANNELS = 1
MODEL_DIR = "WhisperSmall"
OUTPUT_FILE = "transcription.txt"

output_lang_abbr = ""

# Language mapping (WhisperModel uses slightly different abbreviations than MeloTTS)
LANGUAGES = {
    "EN": "en",
    "ES": "es",
    "FR": "fr",
    "ZH": "zh-cn",
    "JP": "ja",
    "KR": "ko"
}

# Queue to store audio chunks
audio_queue = queue.Queue()

# Load Whisper model
model = WhisperModel(MODEL_DIR, device="cuda")  # or "cpu"

# Translator for output language
translator = Translator()

def audio_callback(indata, frames, time_info, status):
    if status:
        print(status)
    audio_queue.put(indata.copy().flatten())

def save_wav(filename, audio):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

def transcribe_audio(audio, input_lang_code, output_lang_code):
    tmp_file = "full_recording.wav"
    save_wav(tmp_file, audio)
    
    # Step 1: Transcribe
    segments, _ = model.transcribe(tmp_file, language=input_lang_code, task="transcribe")
    text = " ".join([seg.text for seg in segments])
    
    # Step 2: Translate if needed
    if output_lang_code != input_lang_code:
        translated = translator.translate(text, src=input_lang_code, dest=output_lang_code)
        text = translated.text
    
    return text

def main():
    print("Translation App - Select from these languages:")
    print("EN - English\nES - Spanish\nFR - French\nZH - Chinese\nJP - Japanese\nKR - Korean")

    input_lang_abbr = input("Input Language (abbreviation): ").upper()
    output_lang_abbr = input("Output Language (abbreviation): ").upper()

    # Validate and map abbreviations
    if input_lang_abbr not in LANGUAGES or output_lang_abbr not in LANGUAGES:
        print("Invalid language selection.")
        return

    input_lang_code = LANGUAGES[input_lang_abbr]
    output_lang_code = LANGUAGES[output_lang_abbr]

    print("\nRecording... Press Ctrl+C to stop.")
    
    try:
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16', callback=audio_callback):
            while True:
                sd.sleep(100)
    except KeyboardInterrupt:
        print("\nRecording stopped.")

    # Gather all audio chunks
    audio_chunks = []
    while not audio_queue.empty():
        audio_chunks.append(audio_queue.get())

    if not audio_chunks:
        print("No audio captured.")
        return

    full_audio = np.concatenate(audio_chunks)

    print("Transcribing and translating...")
    text = transcribe_audio(full_audio, input_lang_code, output_lang_code)

    print("\n--- Full Transcription/Translation ---\n")
    print(text)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"\nSaved transcription/translation to {OUTPUT_FILE}")

    return output_lang_abbr # Returning here so we can use it later in the main pipeline

if __name__ == "__main__":
    main()
