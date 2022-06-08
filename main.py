#!/usr/bin/python
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
from mutagen.easyid3 import EasyID3
import mutagen.id3
import mutagen
import api
import time
import os

#Start Server
api.start_server()
#Login With Phone
try:
    resp,c = api.phone_login()
except api.requests.exceptions.ConnectionError:
    api.start_server()
    time.sleep(2)
    resp,c = api.phone_login()
time.sleep(3)
total=0
now=0
dl_list = []
home_dir = str(os.getcwd())
sel1 = input("欢迎！\n输入1：下载歌单\n输入2：下载专辑\n输入3：下载歌手的全部歌曲\n输入4：下载单曲\n输入5：下载关注的所有歌手的所有歌曲\n你的选择是：")
sel3 = input("是否写入封面（y/n）")

os.system("rm -rf "+home_dir+"/tmp")
os.system("mkdir "+home_dir+"/tmp")


def download_song(id):
    global dl_list
    url = api.get_song_url(id, c)

    if str(url).endswith(".flac"):
        file_type = ".flac"
    else:
        file_type = ".mp3"
    tmp_song = "./tmp/song_tmp" + file_type
    os.system("aria2c "+str(url)+" -o " + tmp_song)
    
    os.system("cp "+tmp_song+" ~/Code/")
    if sel3 == 'y':
        pic_url = api.get_song_pic(id,c)
        picPath = './tmp/cover.jpg'
        os.system("aria2c "+pic_url+" -o " + picPath)
    songFile = ID3()
    if sel3=='y':
        with open(picPath, 'rb') as f:
            picData = f.read()
        if file_type==".mp3":
            songFile['APIC'] = APIC(  # 插入封面
                encoding=0,
                mime='image/jpeg',
                type=3,
                desc='',
                data=picData
            )

    songFile['TIT2'] = TIT2(  # 插入歌名
        encoding=3,
        text=api.get_song_name(id,c)
    )
    songFile['TPE1'] = TPE1(  # 插入第一演奏家、歌手、等
        encoding=3,
        text=api.get_song_artist_name(id,c)
    )
    songFile['TALB'] = TALB(  # 插入专辑名
        encoding=3,
        text=api.get_song_album_name(id,c)
    )
    songFile.save(tmp_song)
    if sel3=='y':
        if file_type == ".flac":
            os.system("metaflac --import-picture-from="+picPath+" "+tmp_song)
    print(str(os.system("pwd")))
    if str(os.system("pwd")).endswith("Api"):
        os.chdir("..")
    os.system("cp "+home_dir+"/tmp/song_tmp"+file_type+" ./Downloads/")
    os.system("mv "+home_dir+"/Downloads/song_tmp"+file_type+" \""+home_dir+"/Downloads/"+api.get_song_artist_name(id,c)+" -- "+api.get_song_name(id,c)+file_type+"\"")
    dl_list.append(api.get_song_name(id,c))
    os.system("rm "+home_dir+"/tmp/*")
    global now
    now=now+1
    
    print(str(total)+" / "+str(now))
    print(os.system("du -h ./Downloads"))
    print(url)





if sel1 == '1':
    tracks = api.get_playlist_track(input('请输入歌单ID：'),c)
    for i in range(len(tracks)):
        download_song(tracks[i])


if sel1 == '2':
    tracks = api.get_album_track(input('请输入专辑ID：'),c)
    for i in range(len(tracks)):
        download_song(tracks[i])


if sel1 == '3':
        albums = api.get_artist_album(input('请输入艺术家ID：'),c)
        for i in range(len(albums)):
            tracks = api.get_album_track(albums[i],c)
            for j in range(len(tracks)):
                total=total+1
        for i in range(len(albums)):
            tracks = api.get_album_track(albums[i],c)
            for j in range(len(tracks)):
                download_song(tracks[j])

if sel1 == '4':
        tracks = input('请输入歌曲ID：')
        download_song(tracks)

if sel1 == '5':
        id_list = input("请输入艺术家ID，以“,”间隔： ").split(",")
        for j in id_list:
            albums = api.get_artist_album(j,c)
            for i in range(len(albums)):
                tracks = api.get_album_track(albums[i],c)
                for k in range(len(tracks)):
                    total=total+1
        print(total)
        for j in id_list:
            albums = api.get_artist_album(j,c)
            for i in range(len(albums)):
                tracks = api.get_album_track(albums[i],c)
                for k in range(len(tracks)):
                    download_song(tracks[k])

print("Finish! ")
sel5=input("Copy or Exit(c/e):  ")
if sel5=='c':
    sel4=input("Copy Musics to:  ")
    os.system("cp "+home_dir+"/Downloads/* "+str(sel4))
    print("Exit!  Bye!")
else:
    print("Exit!  Bye!")