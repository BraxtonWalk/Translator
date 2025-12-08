from kokoro import KPipeline
 
LANGUAGES = {
    "EN": "a",
    "ES": "e",
    "FR": "f",
    "ZH": "z",
    "JP": "j"
}


def main(text: str, inputLang: str = "EN"):
   
    #Access language to turn into audio
    lang_code = LANGUAGES[inputLang]
    print("Language:", lang_code)
    print("Text:", text)

    #Initializes Kokor Model
    pipeline = KPipeline(lang_code=lang_code)

    #Calls Kokor model and sends through text to then be spoken
    generator = pipeline(text, voice='am_eric')
    filename = ""

    # Saving audio 
    for i, (gs, ps, audio) in enumerate(generator):
        print(i, gs, ps)
        filename = f'translation.wav'
       ## display(Audio(data=audio, rate=24000))
        sf.write(filename, audio, 24000)
    print("Audio Saved....")
    

if __name__ == "__main__":
    main("This is a test")
