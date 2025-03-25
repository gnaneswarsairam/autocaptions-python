 
 # Video Subtitle Generator

This is a Python script for extracting audio from a video file, converting it to text using automatic speech recognition, and generating subtitle files.

# What This Code Does
Extracts audio from the video (Eng_speech.mp4).

Converts the audio from MP3 to WAV format.

Splits the audio into small chunks whenever there is silence.

Uses Google Speech Recognition to convert speech into text.

Generates a subtitle (output.srt) file in the correct format.

Cleans up temporary files.


## Usage

1. Place the video file "Eng_speech.mp4" in the same directory as the script.
2. Run the script.
3. The script will extract the audio from the video and save it as "Audio.mp3".
4. The "Audio.mp3" file will be converted to "Audio.wav" using FFmpeg.
5. The script will split the audio into chunks based on silence intervals.
6. Each chunk will be transcribed using the Google speech recognition engine.
7. Subtitles will be generated for each chunk and saved in "output.srt".


## Cleanup

After generating the subtitle file, the script will remove all the temporary chunk files that were created during the process.

Please note that this script assumes the presence of a video file named "Eng_speech.mp4" in the same directory. Adjust the file name accordingly if necessary.

## License

This script is released under the MIT license. Feel free to modify and use it according to your requirements.




