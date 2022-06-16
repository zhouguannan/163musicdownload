import requests
import os 
import _thread
import config
import json

def open_server(text1,text2):
    print(text1+text2)
    os.system("node ./app.js")

def start_server():
    _thread.start_new_thread(open_server,("Server", " Started"))

def phone_login():
    resp = requests.get("http://localhost:3000/login/cellphone?phone=" + config.phone + "&password=" + config.passwd)
    return resp.text,resp.cookies

def code_login():
    os.system("firefox http://localhost:3000/qrlogin.html")

    

def get_username(text):
    decoded = json.loads(text)
    username = decoded["profile"]["nickname"]
    return username

def get_uid(text):
    decoded = json.loads(text)
    uid = decoded["profile"]["userId"]
    return uid
    
def get_user_image(text):
    decoded = json.loads(text)
    image_url = decoded["profile"]["avatarUrl"]
    return image_url

def get_user_description(uid,cookies):
    resp = requests.get(url="http://localhost:3000/user/detail?uid="+str(uid),cookies=cookies)
    decoded = json.loads(resp.text)
    return decoded["profile"]["signature"]

def get_song_url(song_id,cookies):
    resp = requests.get(url="http://localhost:3000/song/url?id="+str(song_id),cookies=cookies)
    decoded = json.loads(resp.text)
    return decoded["data"][0]["url"]

def is_song_flac(song_id,cookies):
    resp = requests.get(url="http://localhost:3000/song/url?id="+str(song_id),cookies=cookies)
    decoded = json.loads(resp.text)
    type1 = decoded["data"][0]["type"]
    print(type1)
    return type1=="flac"

def get_song_name(song_id,cookies):
    resp = requests.get(url="http://localhost:3000/song/detail?ids="+str(song_id),cookies=cookies)
    decoded = json.loads(resp.text)
    return decoded["songs"][0]["name"]

def get_song_pic(song_id,cookies):
    resp = requests.get(url="http://localhost:3000/song/detail?ids="+str(song_id),cookies=cookies)
    decoded = json.loads(resp.text)
    return decoded["songs"][0]["al"]["picUrl"]

def get_song_artist_id(song_id,cookies):
    resp = requests.get(url="http://localhost:3000/song/detail?ids="+str(song_id),cookies=cookies)
    decoded = json.loads(resp.text)
    return decoded["songs"][0]["ar"][0]["id"]

def get_song_artist_name(song_id,cookies):
    resp = requests.get(url="http://localhost:3000/song/detail?ids="+str(song_id),cookies=cookies)
    decoded = json.loads(resp.text)
    output = ""
    count = 0
    count2 = 1
    artist = decoded["songs"][0]["ar"]
    for i in artist:
        count = count + 1
    print(count)
    if count > 1: 
        for i in artist:
            if count2 <= count - 1:
                output = output + i['name'] + " / "
            if count2 == count :
                output = output + i['name']
            count2 = count2 + 1
    elif count == 1:
        output = i['name']
    return output
    
        

def get_song_album_id(song_id,cookies):
    resp = requests.get(url="http://localhost:3000/song/detail?ids="+str(song_id),cookies=cookies)
    decoded = json.loads(resp.text)
    return decoded["songs"][0]["al"]["id"]

def get_song_album_name(song_id,cookies):
    resp = requests.get(url="http://localhost:3000/song/detail?ids="+str(song_id),cookies=cookies)
    decoded = json.loads(resp.text)
    return decoded["songs"][0]["al"]["name"]

def get_song_lyric(song_id,cookies):
    resp = requests.get(url="http://localhost:3000/lyric?id="+str(song_id),cookies=cookies)
    decoded = json.loads(resp.text)
    return decoded["lrc"]["lyric"]

def get_playlist_name(playlist_id,cookies):
    resp = requests.get(url="http://localhost:3000/playlist/detail?id="+str(playlist_id),cookies=cookies)
    decoded = json.loads(resp.text)
    return decoded['playlist']['name']

def get_playlist_cover(playlist_id,cookies):
    resp = requests.get(url="http://localhost:3000/playlist/detail?id="+str(playlist_id),cookies=cookies)
    decoded = json.loads(resp.text)
    return decoded['playlist']['coverImgUrl']

def get_playlist_description(playlist_id,cookies):
    resp = requests.get(url="http://localhost:3000/playlist/detail?id="+str(playlist_id),cookies=cookies)
    decoded = json.loads(resp.text)
    return decoded['playlist']['description']

def get_playlist_tag(playlist_id,cookies):
    resp = requests.get(url="http://localhost:3000/playlist/detail?id="+str(playlist_id),cookies=cookies)
    decoded = json.loads(resp.text)
    return decoded['playlist']['tags']

def get_playlist_track(playlist_id,cookies):
    resp = requests.get(url="http://localhost:3000/playlist/detail?id="+str(playlist_id),cookies=cookies)
    decoded = json.loads(resp.text)
    tracks =  decoded['playlist']['tracks']
    out = {}
    count = 0
    for i in tracks:
        out[count] = i['id']
        count=count+1
    return out
 
def get_album_name(album_id,cookies):
    resp = requests.get(url="http://localhost:3000/album?id="+str(album_id),cookies=cookies)
    decoded = json.loads(resp.text)
    return decoded['songs'][0]['al']['name']

def get_album_cover(album_id,cookies):
    resp = requests.get(url="http://localhost:3000/album?id="+str(album_id),cookies=cookies)
    decoded = json.loads(resp.text)
    return decoded['songs'][0]['al']['picUrl']

def get_album_track(album_id,cookies):
    resp = requests.get(url="http://localhost:3000/album?id="+str(album_id),cookies=cookies)
    decoded = json.loads(resp.text)
    tracks =  decoded['songs']
    out = {}
    count = 0
    for i in tracks:
        out[count] = i['id']
        count=count+1
    return out

def get_artist_album(uid,cookies):
    resp = requests.get(url="http://localhost:3000/artist/album?id="+str(uid)+"&limit=1000",cookies=cookies)
    decoded = json.loads(resp.text)
    print(decoded)
    playlists = decoded['hotAlbums']
    out = {}
    count = 0
    for i in playlists:
        out[count] = i['id']
        count=count+1
    return out

def get_user_playlist(uid,cookies):
    resp = requests.get(url="http://localhost:3000/user/playlist?uid="+str(uid),cookies=cookies)
    decoded = json.loads(resp.text)
    playlists = decoded['playlist']
    out = {}
    count = 0
    for i in playlists:
        out[count] = i['id']
        count=count+1
    return out

def get_artist_all_song(id,cookies):
    resp = requests.get(url="http://localhost:3000/artist/songs?limit=5000&id="+str(id),cookies=cookies)
    decoded = json.loads(resp.text)
    songs = decoded['songs']
    out = {}
    count = 0
    for i in songs:
        out[count] = i['id']
        count=count+1
    return out


