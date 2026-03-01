from pytube import YouTube
from pytube import Playlist
import os
#import ssl #for catching error (ssl error)

#playList
#https://www.youtube.com/playlist?list=PLp7Wxgm0D8s_rqIw-ZYlMnOW1gSWHZM3l
#single:
#D:\music\newSongs
#D:\songs
def removeLastChar(string):
    LENGTH = len(string)
    string = string[0:LENGTH-1]
    return string

def saveYouTubeAudio(url):
    yt = YouTube(url)
    #because there is a problem in the libarary
    while True:
        try:
            video = yt.streams.filter(only_audio=True).first()
            downloaded_file = video.download()
            break
        except:
            print("[SYSTEM] reTrying...")
    base, ext = os.path.splitext(downloaded_file)
    new_file = base + '.mp3'
    print (new_file)
    if (os.path.exists(new_file)==False):
        os.rename(downloaded_file, new_file)
        return True
    else:
        mp4_to_delete = removeLastChar(new_file)
        mp4_to_delete+='4'
        os.remove(mp4_to_delete)
        return False  


def playListYouTube(playlist):
    i=1
    for url in playlist:
        if (saveYouTubeAudio(url)):
            print(f"Finished! {i}/{len(playlist)}")
        else:
            print(f"skeeped {i}/{len(playlist)} because it is already exists")
        i+=1
        

def main():
    num = int(input("if you want playlist enter 1\nif you want single song enter 2\n"))
    if num==1:
        playlistString = input ("enter YouTube playlist URL:\n")
        directory = input ("enter directory name:\n")
        os.chdir(directory)
        playListYouTube(Playlist(playlistString))
    elif num==2:
        url = input ("enter YouTube URL:\n")
        directory = input ("enter directory name:\n")
        os.chdir(directory)
        if(saveYouTubeAudio(url)):
            print("Finished!")
        else:
            print("Skeeped because already exists")
    else:
        raise Exception("invalid input! Try again with valid one")
        
    
    

if __name__ == "__main__":
    main()