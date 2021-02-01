# download-from-youtube
Download multiple audios and videos from Youtube.

## Motivation
I have always wanted to have a travelling music library on my phone/portable music player. These are some of the songs I like listening to very frequently. More often than not, I have access to the web, but there are times when I don't. At these moments, I miss having an offline version of my favourite songs. There are multiple music providers that allow you to download songs for offline use, but a single service will not necessarily have all your favourite songs. And, typically, it is not feasible to subscribe to multiple service providers. To tackle this issue I wrote this package in Python which downloads videos/audios from YouTube which can be added to an offline music library.

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
    * pytube 10.4.1
    * wget 3.2
    * xlrd 1.2.0

## Usage
Use the excel sheet download.xlsx as a template and enter the YouTube link in the appropriate column. In the other columns, enter the download mode (audio/video), title, artists, and album name (all four optional). Save the excel file and run app.py. In the current version audio and video will be saved in the appropriate directories in mp3 and mp4 format, respectively. If a new song needs to be downloaded, the youtube link can be added to the new row in the excel file. There is no need to remove the earlier entries in the excel sheet. Before downloading any new audio/video, the package checks if the file is already downloaded.

## Known issues
* After installing pytube3 and running the code for the first time, you may encounter this error message [`KeyError: 'cipher'`](https://github.com/nficano/pytube/issues/641). To fix this on Windows you can open the file `C:\ProgramData\Miniconda3\Lib\site-packages\pytube\extract.py` as Administrator and replace
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

* 20210201 - Updates. This issue has been resolved in pytube 10.4.1.
 
## TODO
* NLP for extracting title, artist, and album.
