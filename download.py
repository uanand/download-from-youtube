import os
import pandas
import ffmpeg
import wget
from pytube import YouTube

df = pandas.read_excel('download.xlsx',names=['link','mode'])

yt = YouTube('https://www.youtube.com/watch?v=jHNNMj5bNQw')
# thumbnail = wget.download(yt.thumbnail_url)
for stream in yt.streams:
    if (stream.type=='audio'):
        if (stream.mime_type=='audio/mp4' and stream.abr=='128kbps'):
            downloadFileName = stream.default_filename
            newFileName = 'audio'+'/'+downloadFileName.replace('.mp4','.mp3')
            
            print (downloadFileName)
            stream.download()
            
            audio = ffmpeg.input(downloadFileName)
            audio = ffmpeg.output(audio,newFileName)
            ffmpeg.run(audio)
            
            
            
# for link,mode in df.values:
    # print (link,mode)
