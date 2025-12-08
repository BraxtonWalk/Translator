import sounddevice as sd
import numpy as np
import wave
import queue
from faster_whisper import WhisperModel

##############################################################################
# DOES THE SAME THING AS SPEECH TO TEXT. JUST USING IT TO GENERATE SPECTROGRAM
##############################################################################


# Configuration
SAMPLE_RATE = 16000
CHANNELS = 1
OUTPUT_WAV = "spectrogramAudio.wav"
OUTPUT_TXT = "transcription.txt"
WHISPER_MODEL = "small"   # choose: tiny, base, small, medium, large-v3

# Queue to store audio chunks
audio_queue = queue.Queue()

# Load Whisper model
model = WhisperModel(WHISPER_MODEL, device="cuda")   # or "cpu"

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

def transcribe_audio(filename):
    print("Transcribing audio...")
    segments, _ = model.transcribe(filename)
    full_text = " ".join([seg.text for seg in segments])
    return full_text.strip()

def main():
    print("\nRecording... Press Ctrl+C to stop.\n")

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='int16',
            callback=audio_callback
        ):
            while True:
                sd.sleep(100)
    except KeyboardInterrupt:
        print("\nRecording stopped.")

    # Gather chunks
    audio_chunks = []
    while not audio_queue.empty():
        audio_chunks.append(audio_queue.get())

    if not audio_chunks:
        print("No audio captured.")
        return

    # Combine into full audio array
    full_audio = np.concatenate(audio_chunks)

    # Save WAV file
    save_wav(OUTPUT_WAV, full_audio.astype(np.int16))
    print(f"Saved audio to: {OUTPUT_WAV}")

    # Transcribe the audio
    text = transcribe_audio(OUTPUT_WAV)

    # Save text to a file
    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved transcription to: {OUTPUT_TXT}")
    print("\n--- TRANSCRIPTION ---\n")
    print(text)

if __name__ == "__main__":
    main()
