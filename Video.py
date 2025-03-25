# Import necessary libraries
import moviepy.editor as mp  # To extract audio from video
import speech_recognition as sr  # For speech-to-text conversion
import os  # To manage files
import subprocess  # To run system commands
import datetime  # To format timestamps
from pydub import AudioSegment, silence  # For splitting audio

# Set file names
VIDEO_FILE = "Eng_speech.mp4"  # Input video file
AUDIO_MP3 = "Audio.mp3"  # Extracted audio in MP3 format
AUDIO_WAV = "Audio.wav"  # Converted WAV file
SUBTITLE_FILE = "output.srt"  # Output subtitle file


def extract_audio(video_path, audio_mp3, audio_wav):
    """Extracts audio from video and converts it to WAV format."""
    print("Extracting audio from video...")
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_mp3, logger=None)

    print("Converting MP3 to WAV...")
    subprocess.call(["ffmpeg", "-i", audio_mp3, audio_wav, "-y"])  # Convert to WAV


def generate_subtitles(audio_wav, subtitle_file):
    """Converts speech to text and saves subtitles in .srt format."""
    print("Generating subtitles...")
    recognizer = sr.Recognizer()  # Create a recognizer object
    sound = AudioSegment.from_wav(audio_wav)

    # Split audio into chunks based on silence
    chunks = silence.split_on_silence(sound, min_silence_len=500, silence_thresh=sound.dBFS - 14, keep_silence=500)

    # Open subtitle file to write captions
    with open(subtitle_file, "w") as srt_file:
        for i, chunk in enumerate(chunks):
            chunk_path = f"chunk{i}.wav"
            chunk.export(chunk_path, format="wav")  # Save each chunk

            # Recognize speech from the chunk
            with sr.AudioFile(chunk_path) as source:
                audio = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio)  # Convert speech to text
                except sr.UnknownValueError:
                    text = "[Unclear speech]"
                except sr.RequestError:
                    text = "[Speech recognition failed]"

            # Create timestamps for subtitles
            start_time = str(datetime.timedelta(seconds=i * 0.5))[:8]
            end_time = str(datetime.timedelta(seconds=(i + 1) * 0.5))[:8]

            # Write subtitle in SRT format
            srt_file.write(f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n")

            os.remove(chunk_path)  # Delete temporary chunk files

    print("Subtitles saved as:", subtitle_file)


def main():
    """Main function to run the entire process."""
    extract_audio(VIDEO_FILE, AUDIO_MP3, AUDIO_WAV)
    generate_subtitles(AUDIO_WAV, SUBTITLE_FILE)

    # Cleanup temporary files
    os.remove(AUDIO_MP3)
    os.remove(AUDIO_WAV)

    print("\n✅ Subtitle generation complete! Check 'output.srt' file.")


# Run the script
if __name__ == "__main__":
    main()
