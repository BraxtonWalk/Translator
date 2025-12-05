from kokoro import KPipeline
import numpy as np
import torch
import simpleaudio as sa
from IPython.display import display, Audio
import soundfile as sf

# Replace 'your_audio_file.mp3' with the actual path to your audio file
 
LANGUAGES = {
    "EN": "a",
    "ES": "e",
    "FR": "f",
    "ZH": "z",
    "JP": "j"
}

def play_audio_raw(audio, sample_rate=24000):
    if isinstance(audio, torch.Tensor):
        audio = audio.detach().cpu().numpy()

    audio_int16 = (audio * 32767).astype(np.int16)

    play_obj = sa.play_buffer(audio_int16, 1, 2, sample_rate)
    play_obj.wait_done()


def main(text: str, inputLang: str = "EN"):
    lang_code = LANGUAGES[inputLang]
    print("Language:", lang_code)
    print("Text:", text)
    pipeline = KPipeline(lang_code=lang_code)
    generator = pipeline(text, voice='af_heart')
    filename = ""
    for i, (gs, ps, audio) in enumerate(generator):
        print(i, gs, ps)
        filename = f'translation.wav'
       ## display(Audio(data=audio, rate=24000))
        sf.write(filename, audio, 24000)
    print("out of For loop")
    

if __name__ == "__main__":
    main("This is a test")
