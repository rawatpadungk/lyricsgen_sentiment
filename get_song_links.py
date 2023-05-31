from bs4 import BeautifulSoup
import re
from urllib import request

def artist_name():
    real_artist = input("Enter the name of the artist: ")
    artist = real_artist.lower()
    if artist.startswith("the"):
        artist = artist[3:]
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    return real_artist, artist

def give_url(song_title):
    url_lyrics = "https://www.azlyrics.com/lyrics/" + artist + "/" + song_title + ".html"
    return url_lyrics

real_artist, artist = artist_name()
if artist == 'beyounce':
    url_artist = 'https://www.azlyrics.com/k/knowles.html'
elif artist == 'cardib':
    artist = 'cardi-b'
    url_artist = "https://www.azlyrics.com/" + artist[:1] + "/" + artist + ".html"
else:
    url_artist = "https://www.azlyrics.com/" + artist[:1] + "/" + artist + ".html"

page = request.urlopen(url_artist).read()
soup = BeautifulSoup(page, 'html.parser')
songs = soup.findAll("div", {"class":"listalbum-item"})
f = open("songs.txt", "w+")
for song in songs:
    f.write(song.text+"\n")

f.close()

f = open("songs.txt", "r")
f1 = f.readlines()
f2 = open("txt_links/" + artist + "_links.txt", "w+")

f2.write(real_artist+"\n")
for x in f1:
    song_title = re.sub('[^A-Za-z0-9]+', "", x)
    song_title = song_title.lower()
    url = give_url(song_title)
    f2.write(x.rstrip() + " " + url + "\n")

f.close()
f2.close()