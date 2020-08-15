import os
import numpy
import ffmpeg
from pytube import YouTube
from mutagen.mp3 import MP3
from mutagen.id3 import ID3,APIC
from mutagen.easyid3 import EasyID3

########################################################################
def isnan(x):
    """ NumPy equivalent of isnan. Works for all datatypes of x
    (str/list/dictionary). Returns True only if x is of the following
    x = numpy.nan
    x = [numpy.nan]
    x = (numpy.nan)
    x = array([nan])
    
    Parameters:
    ----------
    x : any python supported data type
    
    Usage:
    -----
    utils.isnan(x)
    
    Returns:
    -------
    BOOL
    """
    
    try:
        if (numpy.isnan(x)):
            return True
        else:
            return False
    except:
        return False
########################################################################

########################################################################
def get_metadata_link(link):
    """ TODO. I plan to use natural language processing to extract
    title, artists, and album from youtube description. In the current
    version title, artist, and album are returned as blank strings.
    
    Parameters:
    ----------
    link : str
        Youtube link of the video/audio that needs to be downloaded.
    
    Usage:
    -----
    utils.get_metadata_link(youtube_link)
    
    Returns:
    -------
    title : str
    artist : str
    album : str
    """
    
    yt = YouTube(link)
    title = yt.title
    artist,album = '',''
    return title,artist,album
########################################################################

########################################################################
def get_metadata_file(fileName):
    """ If the mp3 or mp4 file already exists, the metadata can be
    extracted from there. TODO - extract metadata for mp4 files. In the
    current version title, artist, and album are returned as blank
    strings.
    
    Parameters:
    ----------
    fileName : str
        Filename with complete path of the mp3 or mp4 file.
        
    Usage:
    -----
    utils.get_metadata_file(filename)
    
    Returns:
    -------
    title : str
    artist : str
    album : str
    """
    
    if ('.mp3' in fileName):
        audio = EasyID3(fileName)
        try:
            title = audio['title'][0]
        except:
            title = ''
        try:
            artist = audio['artist'][0]
        except:
            artist = ''
        try:
            album = audio['album'][0]
        except:
            album = ''
    elif ('.mp4' in fileName):
        title,artist,album = '','',''
    return title,artist,album
########################################################################

########################################################################
def convertFileFormat(source,target,deleteSource=True):
    """ Convert audio mp4 files to mp3 format using ffmpeg library.
    
    Parameters:
    ----------
    source : str
        Source file with full path.
    target : str
        Target file with full path.
    deleteSource : BOOL
        If True, the source will be deleted after conversion.
        
    Usage:
    -----
    utils.convertFileFormat(source,target,deleteSource=True)
    
    Returns:
    -------
    title : str
    artist : str
    album : str
    """
    
    audio = ffmpeg.input(source)
    audio = ffmpeg.output(audio,target)
    ffmpeg.run(audio,quiet=True,overwrite_output=True)
    if (deleteSource==True):
        os.remove(source)
########################################################################

########################################################################
def addMetadata(fileName,thumbnail,title,artist,album):
    """ Add metadata and thumbnail to mp3 and mp4 files (TODO for mp4).
    
    Parameters:
    ----------
    fileName : str
        Source file with complete path.
    thumbnail : str
        Name of the thumbnail image file with full path.
    title : str
    artist : str
    album : str
    
    Usage:
    -----
    utils.convertFileFormat(source,target,deleteSource=True)
    
    Returns:
    -------
    title : str
    artist : str
    album : str
    """
    
    if ('.mp3' in fileName):
        audio = MP3(fileName,ID3=ID3)
        audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(thumbnail,'rb').read()))
        audio.save()
        os.remove(thumbnail)
        
        # ADD TITLE AND ALBUM NAME
        audio = EasyID3(fileName)
        audio['title'] = title
        audio['artist'] = artist
        audio['album'] = album
        audio.save()
########################################################################
