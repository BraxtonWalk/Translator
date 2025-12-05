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

output_lang_abbr = ""

# Language mapping (WhisperModel uses slightly different abbreviations than MeloTTS)
LANGUAGES = {
    "EN": "en",
    "ES": "es",
    "FR": "fr",
    "ZH": "zh-cn",
    "JP": "ja",
}

def main():
    print("Translation App - Select from these languages:")
    print("EN - English\nES - Spanish\nFR - French\nZH - Chinese\nJP - Japanese")

    input_lang_abbr = input("Input Language (abbreviation): ").upper()
    output_lang_abbr = input("Output Language (abbreviation): ").upper()

    # Validate and map abbreviations
    if input_lang_abbr not in LANGUAGES or output_lang_abbr not in LANGUAGES:
        print("Invalid language selection.")
        return

    # input_lang_code = LANGUAGES[input_lang_abbr]
    # output_lang_code = LANGUAGES[output_lang_abbr]


    return input_lang_abbr, output_lang_abbr# Returning here so we can use it later in the main pipeline

if __name__ == "__main__":
    main()
