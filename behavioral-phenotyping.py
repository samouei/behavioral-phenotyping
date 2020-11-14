#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pytube import YouTube 
import os
from pydub.utils import mediainfo
import subprocess


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



