#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pytube import YouTube 


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






