import warnings
import os
import winsound
import sys

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


import Speech2Text as Speech2Text
import langSelect as langSelect
# Run the main speech-to-text pipeline
lang1, lang2 = langSelect.main()


exit_commands = {
    "EN": "exit translation.",
    "ES": "salir de la traducción.",
    "FR": "Quittez la traduction.",
    "ZH": "退出翻译。",
    "JP": "翻訳を終了します。"
}

while(1):

    translated_text, translated_lang = Speech2Text.main(lang1,lang2)

    # Send the text to the correct model
    from kokoroMain import kokoroSpeech
    
    exit_text = exit_commands[translated_lang].lower()

    # Check for exit — text must be spoken BEFORE exiting
    if translated_text.lower() == exit_text:
        sys.exit()

    kokoroSpeech.main(translated_text,translated_lang)
    wav_path = os.path.abspath("translation.wav")
    winsound.PlaySound(wav_path, winsound.SND_FILENAME)
    
    print("MEOW")
    temp_lang = lang2
    lang2 = lang1
    lang1 = temp_lang