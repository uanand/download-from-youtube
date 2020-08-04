import os
import pandas
import ffmpeg
import wget
from pytube import YouTube
from mutagen.mp3 import MP3
from mutagen.id3 import ID3,APIC
from mutagen.easyid3 import EasyID3

df = pandas.read_excel('download.xlsx',names=['link','mode','title','artist','album'])

for link,mode,title,artist,album in df.values:
    fileName = 'audio'+'/'+title+'.mp3'
    if not(os.path.exists(fileName)):
        yt = YouTube(link)
        thumbnailFile = wget.download(yt.thumbnail_url)
        
        for stream in yt.streams:
            if (stream.type=='audio'):
                if (stream.mime_type=='audio/mp4' and stream.abr=='128kbps'):
                    downloadFileName = stream.default_filename
                    
                    stream.download()
                    
                    # convert mp4 to mp3
                    audio = ffmpeg.input(downloadFileName)
                    audio = ffmpeg.output(audio,fileName)
                    ffmpeg.run(audio)
                    os.remove(downloadFileName)
                    
        # ADD COVER
        audio = MP3(fileName,ID3=ID3)
        audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(thumbnailFile,'rb').read()))
        audio.save()
        os.remove(thumbnailFile)
        
        # ADD TITLE AND ALBUM NAME
        audio = EasyID3(fileName)
        audio['title'] = title
        audio['artist'] = artist
        audio['album'] = album
        audio.save()
    
