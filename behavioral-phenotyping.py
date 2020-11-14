#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pytube import YouTube 
import os


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
    # import os
    
    video_filepath = os.path.abspath(video_name)   
    return video_filepath




