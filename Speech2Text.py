import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import wave
import queue
from googletrans import Translator

# Configuration
SAMPLE_RATE = 16000
CHANNELS = 1
MODEL_DIR = "small"
OUTPUT_FILE = "transcription.txt"

LANGUAGES = {
    "EN": "en",
    "ES": "es",
    "FR": "fr",
    "ZH": "zh-cn",
    "JP": "ja",
}
output_lang_abbr = ""

# Language mapping (WhisperModel uses slightly different abbreviations than MeloTTS)

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
    
    print(text)
    # Step 2: Translate if needed
    if output_lang_code != input_lang_code:
        translated = translator.translate(text, src=input_lang_code, dest=output_lang_code)
        text = translated.text
    
    return text

def main(lang1,lang2):
   
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
    lang1_abbr = LANGUAGES[lang1]
    lang2_abbr = LANGUAGES[lang2]
    print("Transcribing and translating...")
    text = transcribe_audio(full_audio, lang1_abbr, lang2_abbr)

    print("\n--- Full Transcription/Translation ---\n")
    print(text)

    return text.strip(), lang2

if __name__ == "__main__":
    main()
