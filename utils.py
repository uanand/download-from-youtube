import numpy
from mutagen.easyid3 import EasyID3

def isnan(x):
    try:
        if (numpy.isnan(x)):
            return True
        else:
            return False
    except:
        return False
    
def get_metadata_link(link):
    title,artist,album = 'title','artist','album'
    return title,artist,album
    
def get_metadata_file(fileName):
    if ('.mp3' in fileName):
        audio = EasyID3(fileName)
        title = audio['title'][0]
        artist = audio['artist'][0]
        album = audio['album'][0]
        # audio.save()
    return title,artist,album
