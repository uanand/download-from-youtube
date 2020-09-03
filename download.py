import os
import pandas
import wget
import utils
from pytube import YouTube

class downloadFromYoutube:
    """ downloadFromYoutube class has the following functions and
    variables
    
    Parameters:
    ----------
    excelName : str
        name of the excel file which has the youtube links.
    audioPreference : str
        Audio file format which you want to download. Default is 'mp4'.
    videoPreference : str
        Video file format which you want to download. Default is 'mp4'.
        
    Methods:
    -------
    checkDownloadRequired()
    downloadAllTracks()
    getAudioTrack()
    refineDataFrame()
    selectBestAudioStream()
    
    Attributes:
    ----------
    df : pandas dataframe
        Has 8 columns in the following order - 
        1. Youtube link
        2. Download mode (audio/video)
        3. Title of the file that will be saved
        4. Artist name(s)
        5. Album name
        6. Default title which is extracted from youtube description or
           the already existing downloaded file.
        7. Default artist
        8. Default album
        
    Usage:
    -----
    import download
    
    # Example 1:
    dp = download.downloadFromYoutube(
            'download.xlsx',\
            audioPreference='webm',\
            videoPreference='mp4')
    All the entries in excel file will be downloaded and saved in the
    respective audio or video folders. For audio, the webm file format
    will be preferred during download and later is converted to mp3. For
    video, mp4 format is preferred.
    
    # Example 2:
    dp = download.downloadFromYoutube('download.xlsx')
    All the entries in excel file will be downloaded and saved in the
    respective audio or video folders. For audio, the mp4 file format
    will be used during download and later is converted to mp3. For
    video, mp4 format is used.
    """
    
    ####################################################################
    def __init__(self,excelName,audioPreference='mp4',videoPreference='mp4'):
        """ Creates attribute variables and downloads the videos as
        audio or video file.
        
        Refines the pandas dataframe, and then downloads the required
        tracks.
        """
        
        self.df = pandas.read_excel(excelName,names=['link','mode','title','artist','album'])
        self.audioPreference = audioPreference
        self.videoPreference = videoPreference
        
        self.refineDataFrame()
        self.downloadAllTracks()
    ####################################################################
    
    ####################################################################
    def refineDataFrame(self):
        """ Refines self.df to set the default download mode as 'audio'
        and creates new entries for default_title, default_artist, and
        default_album to check if fresh download is required.
        
        Usage:
        -----
        self.refineDataFrame()
        
        Returns:
        -------
        NULL
        
        Creates:
        -------
        self.df : pandas dataframe
            Creates 3 new columns default_title, default_artist, and
            default_album from existing download. If no file exists it
            is left blank.
        """
        
        self.df['default_title'] = ''
        self.df['default_artist'] = ''
        self.df['default_album'] = ''
        [row,col] = self.df.shape
        for r in range(row):
            if (utils.isnan(self.df['mode'][r])):
                self.df['mode'][r] = 'audio'
            if (isinstance(self.df['title'][r],str)):
                if (self.df['mode'][r] == 'audio'):
                    if (os.path.exists('audio/'+self.df['title'][r]+'.mp3')):
                        title,artist,album = utils.get_metadata_file('audio/'+self.df['title'][r]+'.mp3')
                    else:
                        title = self.df['title'][r]
                        if not(utils.isnan(self.df['artist'][r])):
                            artist = self.df['artist'][r]
                        if not(utils.isnan(self.df['album'][r])):
                            album = self.df['album'][r]
                elif (self.df['mode'][r] == 'video'):
                    if (os.path.exists('video/'+self.df['title'][r]+'.mp4')):
                        title,artist,album = utils.get_metadata_file('video/'+self.df['title'][r]+'.mp4')
                    else:
                        title = self.df['title'][r]
                        if not(utils.isnan(self.df['artist'][r])):
                            artist = self.df['artist'][r]
                        if not(utils.isnan(self.df['album'][r])):
                            album = self.df['album'][r]
                else:
                    sys.exit('Not a valid mode. Quitting program.')
            else:
                title,artist,album = utils.get_metadata_link(self.df['link'][r])
            if (utils.isnan(self.df['title'][r])):
                self.df['title'][r] = title
            if (utils.isnan(self.df['artist'][r])):
                self.df['artist'][r] = ''
            if (utils.isnan(self.df['album'][r])):
                self.df['album'][r] = ''
            self.df['default_title'][r] = title
            self.df['default_artist'][r] = artist
            self.df['default_album'][r] = album
    ####################################################################
    
    ####################################################################
    def downloadAllTracks(self):
        """ Scans through every row of self.df and downloads track if
        required.
        
        Usage:
        -----
        self.downloadAllTracks()
        
        Returns:
        -------
        NULL
        """
        for link,mode,title,artist,album,default_title,default_artist,default_album in self.df.values:
            if (mode=='audio'):
                fileName = 'audio/'+title+'.mp3'
                default_fileName = 'audio/'+default_title+'.mp3'
                downloadRequiredFlag = self.checkDownloadRequired([fileName,title,artist,album],[default_fileName,default_title,default_artist,default_album])
                if (downloadRequiredFlag==True):
                    print ('Download %s - %s' %(mode,title))
                    self.getAudioTrack(link,title,artist,album)
                else:
                    print ('Skip %s download - %s' %(mode,title))
            elif (mode=='video'):
                fileName = 'video/'+title+'.mp4'
                default_fileName = 'video/'+default_title+'.mp4'
                downloadRequiredFlag = self.checkDownloadRequired([fileName,title,artist,album],[default_fileName,default_title,default_artist,default_album])
                if (downloadRequiredFlag==True):
                    print ('Download %s - %s' %(mode,title))
                    self.getVideoTrack(link,title,artist,album)
                else:
                    print ('Skip %s download - %s' %(mode,title))
    ####################################################################
    
    ####################################################################
    def checkDownloadRequired(self,desired_params,default_params):
        """ Scans through every row of self.df and downloads track if
        required.
        
        Usage:
        -----
        self.checkDownloadRequired(\
            [new_title,new_artist,new_album)],\
            [old_title,old_artist,old_album])
            
        Returns:
        -------
        downloadFlag : BOOL
            True if fresh download is required, false otherwise. 
        """
        
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
    ####################################################################
    
    ####################################################################
    def getAudioTrack(self,link,title,artist,album):
        """ Downloads the audio file and converts it to mp3 format. In
        addition to this a thumbnail, title, artist, and album are added
        to the metadata of mp3 file. The name of mp3 is title.mp3.
        
        Usage:
        -----
        self.getAudioTrack(\
            'youtube_link',\
            'title_of_audio',\
            'artist_name',\
            'album_name')
            
        Returns:
        -------
        NULL
        """
        
        yt = YouTube(link)
        thumbnailFile = wget.download(yt.thumbnail_url,bar=None,out='thumbnail.jpg')
        fileName = 'audio/'+title+'.mp3'
        itag = self.selectBestAudioStream(yt)
        stream = yt.streams.get_by_itag(itag)
        downloadFileName = stream.default_filename
        stream.download()
        utils.convertFileFormat(downloadFileName,fileName)
        utils.addMetadata(fileName,thumbnailFile,title,artist,album)
    ####################################################################
    
    ####################################################################
    def selectBestAudioStream(self,yt):
        """ Selects the highest quality audio track in the given
        audioPreference format. The input parameter is youtube object
        (yt) that can be created using the pytube3 library.
        
        from pytube import YouTube
        yt = YouTube('youtube link')
        
        Usage:
        -----
        self.selectBestAudioStream(yt)
        
        Returns:
        -------
        itag : int
            Tag of the youtube stream with the highest audio quality.
        """
        
        bitRate = 0
        for stream in yt.streams:
            if (stream.type=='audio'):
                if (self.audioPreference in stream.mime_type):
                    if (int(stream.abr.split('kbps')[0]) > bitRate):
                        itag = stream.itag
                        bitRate = int(stream.abr.split('kbps')[0])
        return itag
    ####################################################################
    
    ####################################################################
    def getVideoTrack(self,link,title,artist,album):
        """ Downloads the video and converts it to mp4 format. In
        addition to this a thumbnail, title, artist, and album are added
        to the metadata of mp4 file. The name of mp4 is title.mp4.
        
        Usage:
        -----
        self.getVideoTrack(\
            'youtube_link',\
            'title_of_video',\
            'artist_name',\
            'album_name')
            
        Returns:
        -------
        NULL
        """
        
        yt = YouTube(link)
        thumbnailFile = wget.download(yt.thumbnail_url,bar=None)
        fileName = 'video/'+title+'.mp4'
        itag = self.selectBestVideoStream(yt)
        stream = yt.streams.get_by_itag(itag)
        downloadFileName = stream.default_filename
        stream.download()
        utils.convertFileFormat(downloadFileName,fileName)
        utils.addMetadata(fileName,thumbnailFile,title,artist,album)
    ####################################################################
    
    ####################################################################
    def selectBestVideoStream(self,yt):
        """ Selects the highest quality audio track in the given
        audioPreference format. The input parameter is youtube object
        (yt) that can be created using the pytube3 library.
        
        from pytube import YouTube
        yt = YouTube('youtube link')
        
        Usage:
        -----
        self.selectBestVideoStream(yt)
        
        Returns:
        -------
        itag : int
            Tag of the youtube stream with the highest video quality.
        """
        
        resolution,fps = 0,0
        for stream in yt.streams:
            if (stream.type=='video'):
                if (self.videoPreference in stream.mime_type):
                    if (stream.resolution != None):
                        if ((int(stream.resolution.split('p')[0]) > resolution) and (stream.fps > fps)):
                            itag = stream.itag
                            resolution = int(stream.resolution.split('p')[0])
                            fps = stream.fps
        return itag
    ####################################################################
