import warnings
import os
import winsound
import sys

# Suppress all FutureWarnings and UserWarnings globally
warnings.filterwarnings("ignore")

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

    #Call Speech2Text.py
    translated_text, translated_lang = Speech2Text.main(lang1,lang2)

    # Send the text to the correct model
    from kokoroMain import kokoroSpeech
    
    # Check is text matches a exit command to close program
    exit_text = exit_commands[translated_lang].lower()

    # Check for exit — text must be spoken BEFORE exiting
    if translated_text.lower() == exit_text:
        sys.exit()

    #call text to speech model
    kokoroSpeech.main(translated_text,translated_lang)
    wav_path = os.path.abspath("translation.wav")
    winsound.PlaySound(wav_path, winsound.SND_FILENAME)
    
    # Debug print
    print("MEOW")

    #Switch languages so next speaker can talk
    temp_lang = lang2
    lang2 = lang1
    lang1 = temp_lang