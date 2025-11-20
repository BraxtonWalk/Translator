from melo.api import TTS
from simpleaudio import WaveObject

speed = 1.0
device = 'cuda'

def translate(text):
    model = TTS(language='ES', device=device)
    speaker_ids = model.hps.data.spk2id
    output_path = 'Audio_Outputs/es.wav'
    model.tts_to_file(text, speaker_ids['ES'], output_path, speed=speed)
    return output_path

def playSound(path):
    WaveObject.from_wave_file(path).play().wait_done()

def main(text):
    path = translate(text)
    playSound(path)
