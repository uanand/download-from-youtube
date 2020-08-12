import utils
import os
import pandas
import numpy
import ffmpeg
import wget
from pytube import YouTube
from mutagen.mp3 import MP3
from mutagen.id3 import ID3,APIC
from mutagen.easyid3 import EasyID3

class downloadFromYoutube:
    
    def __init__(self,excelName):
        self.names = ['link','mode','title','artist','album']
        self.df = pandas.read_excel(excelName,names=self.names)
        
        self.refineDataFrame()
        self.download()
        
    def refineDataFrame(self):
        self.df['default_title'] = 'title'
        self.df['default_artist'] = 'artist'
        self.df['default_album'] = 'album'
        [row,col] = self.df.shape
        for r in range(row):
            if (utils.isnan(self.df['mode'][r])):
                    self.df['mode'][r] = 'audio'
            if (os.path.exists('audio/'+self.df['title'][r]+'.mp3')):
                title,artist,album = utils.get_metadata_file('audio/'+self.df['title'][r]+'.mp3')
            elif (os.path.exists('video/'+self.df['title'][r]+'.mp4')):
                title,artist,album = utils.get_metadata_file('video/'+self.df['title'][r]+'.mp4')
            else:
                title,artist,album = utils.get_metadata_link(self.df['link'][r])
            if (utils.isnan(self.df['title'][r])):
                self.df['title'][r] = title
            if (utils.isnan(self.df['artist'][r])):
                self.df['artist'][r] = artist
            if (utils.isnan(self.df['album'][r])):
                self.df['album'][r] = album
            self.df['default_title'][r] = title
            self.df['default_artist'][r] = artist
            self.df['default_album'][r] = album
            
    def download(self):
        for link,mode,title,artist,album,default_title,default_artist,default_album in self.df.values:
            if (mode=='audio'):
                fileName = 'audio/'+title+'.mp3'
                default_fileName = 'audio/'+default_title+'.mp3'
                downloadRequiredFlag = self.checkDownloadRequired([fileName,title,artist,album],[default_fileName,default_title,default_artist,default_album])
                if (downloadRequiredFlag==True):
                    self.getAudioTrack(link,title,artist,album)
                    
                    
    def checkDownloadRequired(self,desired_params,default_params):
        downloadFlag = False
        if (os.path.exists(desired_params[0])==False):
            downloadFlag = True
        if (desired_params[0]!= default_params[0] or\
            desired_params[1]!= default_params[1] or\
            desired_params[2]!= default_params[2] or\
            desired_params[3]!= default_params[3]):
                downloadFlag = True
        if (downloadFlag==True):
            if (os.path.exists(desired_params[0])):
                os.remove(desired_params[0])
            if (os.path.exists(default_params[0])):
                os.remove(default_params[0])
        return downloadFlag
        
    def getAudioTrack(self,link,title,artist,album):
        yt = YouTube(link)
        thumbnailFile = wget.download(yt.thumbnail_url)
        fileName = 'audio/'+title+'.mp3'
        
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
        
        
        
        

# df = pandas.read_excel('download.xlsx',names=['link','mode','title','artist','album'])

# for link,mode,title,artist,album in df.values:
    # fileName = 'audio'+'/'+title+'.mp3'
    # if not(os.path.exists(fileName)):
        # yt = YouTube(link)
        # thumbnailFile = wget.download(yt.thumbnail_url)
        
        # for stream in yt.streams:
            # if (stream.type=='audio'):
                # if (stream.mime_type=='audio/mp4' and stream.abr=='128kbps'):
                    # downloadFileName = stream.default_filename
                    
                    # stream.download()
                    
                    # # convert mp4 to mp3
                    # audio = ffmpeg.input(downloadFileName)
                    # audio = ffmpeg.output(audio,fileName)
                    # ffmpeg.run(audio)
                    # os.remove(downloadFileName)
                    
        # # ADD COVER
        # audio = MP3(fileName,ID3=ID3)
        # audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(thumbnailFile,'rb').read()))
        # audio.save()
        # os.remove(thumbnailFile)
        
        # # ADD TITLE AND ALBUM NAME
        # audio = EasyID3(fileName)
        # audio['title'] = title
        # audio['artist'] = artist
        # audio['album'] = album
        # audio.save()
