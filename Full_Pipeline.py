import warnings

# Suppress all FutureWarnings and UserWarnings globally
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Now import libraries that might trigger warnings
from huggingface_hub import logging as hf_logging
hf_logging.set_verbosity_error()

from transformers import logging as transformers_logging
transformers_logging.set_verbosity_error()

from tqdm import tqdm
tqdm.tqdm = lambda *args, **kwargs: args[0]  # disables progress bars


import Speech2Text
from MeloTTS.translation_scripts import EnglishTranslation as english_main
from MeloTTS.translation_scripts import SpanishTranslation as spanish_main
from MeloTTS.translation_scripts import FrenchTranslation as french_main
from MeloTTS.translation_scripts import ChineseTranslation as chinese_main
from MeloTTS.translation_scripts import JapaneseTranslation as japanese_main
from MeloTTS.translation_scripts import KoreanTranslation as korean_main

# Run the main speech-to-text pipeline
translated_lang = Speech2Text.main()

# Read the transcription
file_path = "transcription.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    translated_text = file.read()

# Send the text to the correct model
match translated_lang:
    case "EN":
        english_main.main(translated_text)
    case "ES":
        spanish_main.main(translated_text)
    case "FR":
        french_main.main(translated_text)
    case "ZH":
        chinese_main.main(translated_text)
    case "JP":
        japanese_main.main(translated_text)
    case "KR":
        korean_main.main(translated_text)