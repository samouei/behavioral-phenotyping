#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pytube import YouTube 
import os
from pydub.utils import mediainfo
import subprocess
import math


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





