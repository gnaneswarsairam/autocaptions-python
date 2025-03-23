import moviepy.editor as mp
import speech_recognition as sr
import subprocess
from pydub import AudioSegment, silence
import os, datetime

# Extract audio from video
video = mp.VideoFileClip("Eng_speech.mp4")
video.audio.write_audiofile("Audio.mp3")

# Convert MP3 to WAV
subprocess.call(['ffmpeg', '-i', 'Audio.mp3', 'Audio.wav'])

# Initialize recognizer
recognizer = sr.Recognizer()
sound = AudioSegment.from_wav("Audio.wav")
chunks = silence.split_on_silence(sound, min_silence_len=500, silence_thresh=sound.dBFS-14, keep_silence=500)

# Generate subtitles
with open('output.srt', 'w') as subtitle_file:
    for i, chunk in enumerate(chunks):
        chunk_path = f"chunk{i}.wav"
        chunk.export(chunk_path, format="wav")
        with sr.AudioFile(chunk_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_sphinx(audio)
            except sr.UnknownValueError:
                text = ""
        
        start_time = str(datetime.timedelta(seconds=i*0.5))[:8]
        end_time = str(datetime.timedelta(seconds=(i+1)*0.5))[:8]
        
        subtitle_file.write(f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n")
        os.remove(chunk_path)

# Cleanup temporary files
os.remove("Audio.mp3")
os.remove("Audio.wav")
