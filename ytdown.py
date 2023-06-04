#!python3
# Usage -
# 1. open cmd
# 2. cd to the folder where these files are present
# 3. type - python ytdown.py
# the script will start working


import os
import subprocess
from pytube import YouTube
import random
import requests
import re
import string


#imp functions


def foldertitle(url):

    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False

    plain_text = res.text

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]

    else:
        print('Incorrect attempt.')
        return False

    return cPL



def link_snatcher(url):
    our_links = []
    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False

    plain_text = res.text

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
    else:
        print('Incorrect Playlist.')
        return False

    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, plain_text)

    for m in mat:
        new_m = m.replace('&amp;', '&')
        work_m = 'https://youtube.com/' + new_m
        # print(work_m)
        if work_m not in our_links:
            our_links.append(work_m)

    return our_links


BASE_DIR = os.getcwd()

print('WELCOME TO PLAYLIST DOWNLOADER DEVELOPED BY - www.github.com/mohit0101')

url = str(input("\nspecify you playlist url\n"))

print('\nCHOOSE ANY ONE - TYPE 360P OR 720P OR MP3\n')
user_res = str(input()).lower()


print('...You choosed ' + user_res + ' resolution\n.')

our_links = link_snatcher(url)

os.chdir(BASE_DIR)

new_folder_name = foldertitle(url)
new_folder_name = new_folder_name[:7] if user_res == '360p' or user_res == '720p' else new_folder_name[:7] + '_mp3'
print(new_folder_name)

try:
    os.mkdir(new_folder_name)
except:
    print('folder already exists')

os.chdir(new_folder_name)
SAVEPATH = os.getcwd()
print(f'\n files will be saved to {SAVEPATH}')

x=[]
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        pathh = os.path.join(root, name)

        
        if os.path.getsize(pathh) < 1:
            os.remove(pathh)
        else:
            x.append(str(name))

try:
    Start_point = int(input("Enter a start point, if you want to start download the playlist from the start enter 0:"))
except:
    Start_point = 0

print("the program start download from video number", Start_point)

print('\nconnecting . . .\n')
vid_num =  0
for link in our_links:
    vid_num += 1
    if  vid_num < Start_point:
        continue
    print("",vid_num)
    try:
        yt = YouTube(link)
        main_title = yt.title
        main_title = main_title + '.mp4'
        main_title = main_title.replace('|', '')
        
    except:
        print('connection problem..unable to fetch video info')
        break

    
    if main_title not in x:

        
        if user_res == '360p' or user_res == '720p':
            vid = yt.streams.filter(progressive=True, file_extension='mp4', res=user_res).first()
            print('Downloading. . . ' + vid.default_filename + ' and its file size -> ' + str(round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
            vid.download(SAVEPATH)
            print('Video Downloaded')
        elif user_res == 'mp3':
            vid = yt.streams.filter(only_audio=True).first()
            print('Downloading. . . ' + vid.default_filename + ' and its file size -> ' + str(round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
            out_file = vid.download(SAVEPATH)
            base, ext = os.path.splitext(out_file)
            new_file = base + f'[{vid_num}].mp3'
            os.rename(out_file, new_file)
            print('Song Downloaded')
        else:
            print('something is wrong.. please rerun the script')


    else:
        print(f'\n skipping "{main_title}" video \n')


print(' downloading finished')
print(f'\n all your videos are saved at --> {SAVEPATH}')
