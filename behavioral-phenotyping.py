#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pytube import YouTube 
import os
from pydub.utils import mediainfo
import subprocess
import math
import speech_recognition as sr
from spacy.lang.en import English
from nltk.stem.snowball import SnowballStemmer

# 1.
#### Getting Video ####
def download_video(link):
    '''
    Downloads Youtube videos in the current directory.
    Input: Youtube link as a string.
    Returns: a task completion message (string)
    Method: pytube module
    '''  
    
    # create a YouTube object 
    yt = YouTube(link)
    
    # get the first stream
    stream = yt.streams.first()

    # download video
    stream.download()
    
    video_title = yt.title
    
    print(f"'{video_title}' was downloaded successfully.")


# 2.
#### Preprocessing Video #### 
def get_video_filepath(video_name):
    '''
    Gets the local file path for a video.
    Input: video_name.mp4 as a string.
    Returns: file path (string)
    Method: os module
    '''  
    
    video_filepath = os.path.abspath(video_name)   
    return video_filepath


def get_video_data(video_filepath):
    '''
    Gets the metadata of a video.
    Input: video file path as a string.
    Returns: duration, channels, bit rate, sample rate (tuple)
    Method: mediainfo from pydub.utils module
    '''  
    
    video_data = mediainfo(video_filepath)
    duration = video_data["duration"]
    channels = video_data["channels"]
    bit_rate = video_data["bit_rate"]
    sample_rate = video_data["sample_rate"]
    
    return (duration, channels, bit_rate, sample_rate)


def video_to_audio(video_name, audio_name):
    '''
    Extracts audio from video and .
    Input: video_name.mp4 as a string.
           audio_name.mp3 as a string
    Returns: a task completion message (string)
    Method: ffmpeg, subprocess module
    '''    
    
    command = f"ffmpeg -i" + " " + video_name + " " + audio_name
    subprocess.call(command, shell = True)
    
    print(f"'{video_name}' was converted to audio successfully.")


def split_audio(audio_name, duration, copy_directory, interval):
    '''
    Splits audio into intervals.
    Input: audio_name.mp3 as a string
           duration (int?)
           copy_directory
           interval (seconds)
    Returns: a task completion message (string)
    Method: math module, ffmpeg, subprocess module
    '''     
    
    split_audio_map = {}
    count = 0
    
    # start from the bginning of audio and step with the length of desired interval (sec)
    for i in range(0, math.ceil(float(duration)), interval):
        
        start = i
        end = i + interval
        
        # name the splitted portion (e.g. 'part_0_30.mp3')
        split_file = f"{audio_name[:-4:]}_part{count}_{start}_{end}.mp3"
        
        # ffmpeg command for splitting one portion and copying into the desired directory
        command = f"ffmpeg -ss {start} -i {audio_name} -t {interval} -c copy {copy_directory}/{split_file}"
        
        # keep track of files
        split_audio_map[count] = split_file
        count += 1
        subprocess.call(command, shell=True) 
        
    print(f"\n>>>> '{audio_name}' was converted to {count} audio files successfully.\n>>>> Files can be found in {copy_directory}.\n")



# 3.
#### Calling Speech_to_Text API ####        
def call_speech_to_text_API(audio_name, cloud = False, api_key = None):
    '''
    Sends audio and receives text transcription 
        from the Google Speech-to-Text API service.
    Input: audio_name.wav as a string
           cloud bool (optional)
           api_key string
    Returns: a text transcription (string)
    Method: speech_recognition
    '''          
        
    r = sr.Recognizer() 
    my_audio = sr.AudioFile(audio_name)
    
    # open file, read content, and store data in an AudioFile instance
    with my_audio as source:
        
        # adjust for ambient noise
        r.adjust_for_ambient_noise(source) 
        '''
        reads the first second of the file stream and calibrates the recognizer 
        to the noise level of the audio. Hence, that portion of the stream is consumed 
        before you call record() to capture the data
        '''
        #r.adjust_for_ambient_noise(source, duration=0.5) # to take care of the missing 1 second issue from line above
        
        audio = r.record(source)  
        
    if cloud:
        # open credentials JSON file
        with open({api_key}) as f:
            GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()
                
        try:
            # authenticate call to Google Cloud API and transcribe
            return r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        except sr.UnknownValueError:
            print("Speech is unintelligible.")
        except sr.RequestError:
            print("Speech recognition operation failed. Check credentials and Internet connection.")
            
    else:
        return r.recognize_google(audio)
    
        # to get all transcriptions (raw API response as a JSON dictionary)
        #return r.recognize_google(audio, show_all=True)


# 4.
#### Text Preprocessing ####    
def tokenizer(text, lst = False):
    '''
    Tokenize text (non-destructive tokenization).
    Input: text as a string
           lst bool (optional)        
    Returns: spaCy Doc object (iterable sequence) 
             list (optional)   
    Method: spaCy
    '''     
    
    # create a spaCy nlp object
    nlp = English()
    
    # annotate/tokenize text
    doc = nlp(text)
    
    if lst:
        return [i.text for i in doc]
    else:
        return doc 

    
def lemmatizer(doc):
    '''
    Lemmatizes tokens.
    Input: spaCy Doc object
    Returns: list 
    Method: N/A
    ''' 
    # get lemmatized form of each token
    return [token.lemma_ for token in doc]


def stemmer(doc):
    '''
    Creates stems for each token. 
        Also converts all tokens to lowercase.
    Input: spaCy Doc object
    Returns: list 
    Method: nltk
    ''' 

    snowball = SnowballStemmer(language='english') 
    return [snowball.stem(doc[i]) for i in range(len(doc))]


