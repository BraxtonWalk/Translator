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

# Queue to store audio chunks
audio_queue = queue.Queue()

# Load Whisper model
model = WhisperModel(MODEL_DIR, device="cuda")  # or "cpu"

# Translator for output language
translator = Translator()


#Putting Audio chunks into Queue
def audio_callback(indata, frames, time_info, status):
    if status:
        print(status)
    audio_queue.put(indata.copy().flatten())

#Save audio channel
def save_wav(filename, audio):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

#Takes in the temp file that was created from sound byte
#Takes in the audio file and transcribes it into the input langues text 
#Translates the temporary text into the output language and returns the translated text.
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
    
    #Gets audio recording until a keyboard interrupt happens
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

    #Take all audio chunks and connect them into a single audio stream
    full_audio = np.concatenate(audio_chunks)
    lang1_abbr = LANGUAGES[lang1]
    lang2_abbr = LANGUAGES[lang2]
    print("Transcribing and translating...")

    #Taking full audio stream with the input and output language and sending it to transcribe_audio() function
    text = transcribe_audio(full_audio, lang1_abbr, lang2_abbr)

    print("\n--- Full Transcription/Translation ---\n")
    print(text)

    # Return text and language 2
    return text.strip(), lang2

if __name__ == "__main__":
    main()
