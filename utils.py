import numpy

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
        title,artist,album = 'title','artist','album'
    return title,artist,album
