# Real-Time Audio Translation App

A real-time audio translation system that captures microphone input, converts speech to text, translates the text into a target language, and generates spoken output using text-to-speech. This application is designed for low-latency, cross-lingual communication and can be adapted to various languages, models, and deployment environments.

## Features
- Live microphone capture with streaming buffers
- Speech-to-Text (STT) Faster-Whisper
- Neural Machine Translation (NMT) using Google Translate, Kokoro & custom pipelines
- Text-to-Speech (TTS) output
- Optional transcription logging, language auto-detection, and real-time UI updates

## How to use
- clone the repository (git clone https://github.com/BraxtonWalk/Translator.git)
- open the Full_Pipeline.py
- run the file and follow instructions in terminal
- to change the voice look up voices from kokoro and paste voice in kokoroSpeech.py
- to exit program either hit Ctrl+c twice or say 'Exit translation' in whatever language the program is currently detecting
