# download-from-youtube
Download multiple audios and videos (TODO) from Youtube.

## Introduction
I have always wanted to have a travelling music library on my phone/portable music player. These are some of the songs I like listening to very frequently. More often than not, I have access to the web, but there are times when I don't and at these moments I wish I had songs offline in my phone. In addition to this, when listening to music on YouTube I have to keep the screen on (YouTube offers the premium version but there is usually a limit on the services one can subscribe to).

There are multiple music providers that allow you to download songs for offline use, but a single service will not necessarily have all your favourite songs. And again, it's not feasible to subscribe to all the service providers. To tackle this issue I wrote this package in Python which downloads videos/audios from YouTube which can be added to an offline music library.

## Requirements
* Windows/Debian Linux (Tested on Windows 10, Linux Mint, Ubuntu, and Raspberry Pi OS)
* [ffmpeg](https://ffmpeg.org/). It is easy to install on Debian if you have admin rights. On terminal type -
```
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install ffmpeg
```
On Windows you can download the ffmpeg package from [here](https://ffmpeg.zeranoe.com/builds/) and install using these [instructions](https://www.wikihow.com/Install-FFmpeg-on-Windows).
* Any office package which can edit and save .xlsx files - [Microsoft Office](https://www.office.com)/[Libre Office](https://www.libreoffice.org)/[Open Office](https://www.openoffice.org)/[WPS Office](https://www.wps.com)
* python >= 3.6.9
    * ffmpeg-python 0.2.0
    * mutagen 1.45.1
    * numpy 1.19.1
    * pandas 1.1.0
    * pytube3 9.6.4
    * wget 3.2
    * xlrd 1.2.0
    * Earlier versions of the above packages might work as well (not tested).

## Usage
Use the excel sheet download.xlsx as a template and enter the YouTube link in the appropriate column. In the other columns, enter the download mode (audio/video), title, artists, and album name (all four optional). Save the excel file and run app.py. In the current version audio and video will be saved in the respective directories in mp3 and mp4 format respectively.

## Known issues
After installing pytube3 and running the code for the first time, you may encounter this error message [`KeyError: 'cipher'`](https://github.com/nficano/pytube/issues/641). To fix this on Windows you can open the file `C:\ProgramData\Miniconda3\Lib\site-packages\pytube\extract.py` as Administrator and replace
```
cipher_url = [
parse_qs(formats[i]["cipher"]) for i, data in enumerate(formats)
]
```
with
```
try:
    cipher_url = [
    parse_qs(formats[i]["cipher"]) for i, data in enumerate(formats)
    ]
except:
    cipher_url = [
    parse_qs(formats[i]["signatureCipher"]) for i, data in enumerate(formats)
    ]
```
Be careful with the indentation.

## TODO
* Video download feature.
* NLP for extracting title, artist, and album.
