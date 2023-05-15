'''
Youtube downloader script that can download videos from command line.

USAGE:
python3 ytDownload.py -l '(youtube link)' -r (resolution) -t (download_type)
'''

from pytube import YouTube
from ffmpy import FFmpeg
import argparse
import os

OPATH = 'Videos'

def Download(link, quality, type):
    video = YouTube(link)
    vidname = video.title
    
    if type == 'mp3':
#       Quality is likely not a concern when downloading mp3, get highest
        video = video.streams.get_highest_resolution()
    else:
#        video = video.streams.filter(res=quality).first()
        video = video.streams.get_highest_resolution()
 
    try:
        file = video.download(output_path=OPATH, filename=vidname+'.mp4')
    except:
        print("ERROR")
        return
 
#   Since we can't download audio only in mp3 format,
#   we convert to mp3 using ffmpeg.
#   This also reduces file size dramatically.
    if type == 'mp3':
    
        IN_FILE = OPATH + '/' + vidname + '.mp4'
        OUT_FILE = OPATH + '/' + vidname + '.mp3'
    
        ff = FFmpeg(
            inputs = {IN_FILE: None},
            outputs = {OUT_FILE: None}
        )
        
        ff.run()
        
        try:
            os.remove(IN_FILE)
        except:
            print("Could not remove video portion")



if __name__ == '__main__':

    download_type = ['mp3', 'mp4']

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--Link')
    parser.add_argument('-r', '--Resolution')
    parser.add_argument('-t', '--Type', choices = download_type)

    args = parser.parse_args()

    if args.Link:
        print("Link = ", args.Link)
        
    if args.Resolution:
        print("Resolution = ", args.Resolution)
        
    if args.Type:
        print("Download Type = ", args.Type)

    Download(args.Link, args.Resolution, args.Type)
