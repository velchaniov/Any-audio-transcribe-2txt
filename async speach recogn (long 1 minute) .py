#This script will help to recognize speech from any audio format and any length audio file
# Enhance audio quality for better results
#Write recognized speech into txt file

#ffmpeg (brew install ffmpeg + pip3 install ffmpeg-python) and sox (brew install sox) utilities 

import speech_recognition as sr #pip3 install SpeechRecognition
import os
from pydub import AudioSegment #pip3 install pydub
from pydub import effects
import asyncio #pip3 install pydub
import subprocess

# initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# function to detect audio file format and convert to wav
def convert_to_wav(audio_file):
    extension = os.path.splitext(audio_file)[1]
    if extension not in ['.wav']:
        sound = AudioSegment.from_file(audio_file)
        audio_file = os.path.splitext(audio_file)[0] + '.wav'
        sound.export(audio_file, format="wav")
    return audio_file

#Convert short audio <1 min
async def convert_audio_to_text(audio_file):
    # Reading Audio file as source
    # listening the audio file and store in audio_text variable
    with sr.AudioFile(audio_file) as source:
        audio_text = r.record(source)
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    try:
        #using google speech recognition
        text = await r.recognize_google(audio_text, language='ru-RU') #You can change language for more accurate recognition
        print("The audio file contains: " + text)
        # write text to txt file
        filename = os.path.splitext(audio_file)[0] + '.txt'
        with open(filename, 'w') as f:
            f.write(text)
            f.close()
    except:
        print("Sorry, I did not get that")

#Split audio file >1 min into chunks due to google speech recognition limitations        
def transcribe_long_audio(audio_file):
    # Divide audio file into chunks of less than 1 minute
    audio = AudioSegment.from_wav(audio_file)
    chunk_length_ms = 60 * 1000 # 1 minute
    chunks = make_chunks(audio, chunk_length_ms)

    # Transcribe each chunk and concatenate the results
    transcribed_text = ""
    for i, chunk in enumerate(chunks):
        chunk_filename = "chunk{}.wav".format(i)
        chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_text = r.record(source)
        try:
            text = r.recognize_google(audio_text, language='ru-RU')
            transcribed_text += text
        except:
            print("Sorry, I did not get that")
    filename = os.path.splitext(audio_file)[0] + '.txt'
    with open(filename, 'w') as f:
        f.write(transcribed_text)
        f.close()

def make_chunks(audio, chunk_length):
    """Divide an AudioSegment into chunks."""
    chunks = []
    start = 0
    while start < len(audio):
        chunks.append(audio[start:start+chunk_length])
        start += chunk_length
    return chunks

#Enhance audio quality for better speech recognition results
def voice_cleanup(audio_file):
    try:
        command = ["sox", audio_file, 
               "remix", "-", 
               "highpass", "100", 
               "norm", 
               "compand", "0.05,0.2", "6:-54,-90,-36,-36,-24,-24,0,-12", "0", "-90", "0.1", 
               "vad", "-T", "0.6", "-p", "0.2", "-t", "5", 
               "fade", "0.1", 
               "reverse", 
               "vad", "-T", "0.6", "-p", "0.2", "-t", "5", 
               "fade", "0.1", 
               "reverse", 
               "norm", "-0.5",
               audio_file]
        subprocess.run(command)
    except:
        print("An error occurred while voice cleanup")
    
# main function
if __name__ == '__main__':
    # getting the audio file
    audio_file = input("Enter audio file name (with path): ")
    # check if file exists
    if os.path.isfile(audio_file):
        audio_file = convert_to_wav(audio_file)
        audio = AudioSegment.from_wav(audio_file)
        voice_cleanup(audio_file)
        if len(audio) > 60 * 1000: # 60 seconds
            transcribe_long_audio(audio_file)
        else:
            convert_audio_to_text(audio_file)
    else:
        print("File not found!")
