import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

def read_transcription():
    content = ""
    with open("transcription.txt", "r") as file:
        content = file.read()
    return content


def plot_signal_amp(times, channel, t_audio,audio_text):
    plt.figure(figsize=(15, 5))
    plt.plot(times, channel)
    plt.title(f'Left Channel Amplitude: {audio_text}')
    plt.ylabel('Amplitude')
    plt.xlabel('Time (s)')
    plt.xlim(0, t_audio)
    plt.show()

def plot_spectrogram(channel, sample_freq,audio_text):
    # Compute spectrogram
    freqs, times, Sxx = spectrogram(channel, fs=sample_freq)

    plt.figure(figsize=(15, 5))
    plt.pcolormesh(times, freqs, 10 * np.log10(Sxx), shading='gouraud')
    plt.title(f"Spectrogram (Left Channel): {audio_text}")
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Time (s)")
    plt.colorbar(label="Intensity (dB)")
    plt.tight_layout()
    plt.show()

def main():
    wav_obj = wave.open("spectrogramAudio.wav", 'rb')

    # Sample rate and frame count
    sample_freq = wav_obj.getframerate()
    n_samples = wav_obj.getnframes()
    time_audio = n_samples / sample_freq

    # Read Pulse Code Modulation (PCM) data
    signal_wave = wav_obj.readframes(n_samples)
    signal_array = np.frombuffer(signal_wave, dtype=np.int16)

    # Stereo → separate channels
    l_channel = signal_array[0::2]
    r_channel = signal_array[1::2]

    # Times for amplitude plot
    times = np.linspace(0, time_audio, num=len(l_channel))

    #read in transcription
    audio_to_text = read_transcription()
    # Plot waveform
    plot_signal_amp(times, l_channel, time_audio, audio_to_text)

    # Plot spectrogram using SciPy
    plot_spectrogram(l_channel, sample_freq, audio_to_text)

if __name__ == "__main__":
    main()
