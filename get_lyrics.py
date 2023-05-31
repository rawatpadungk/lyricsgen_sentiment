from bs4 import BeautifulSoup
import urllib
from urllib import request
import time
import re
import random
import glob
from tqdm import tqdm


def get_lyrics(from_dir, to_dir):
    '''
    Example Command:
    python -c 'from get_lyrics import get_lyrics; get_lyrics("txt_links", "txt_generated")'
    '''
    for path in glob.glob(from_dir+'/*.txt'):
        print("START:", path)
        txt_name = re.sub(r'^.*/|_links.*$', '', path)
        get_lyric(from_dir, to_dir, txt_name)
        print("END:", path)
        time.sleep(5)

def get_lyric(from_dir, to_dir, name):
    '''
    Example Command:
    python -c 'from get_lyrics import get_lyric; get_lyric("txt_links", "txt_generated", "justinbieber")'
    '''
    f = open(from_dir + '/' + name + '_links.txt', "r")
    f1 = f.readlines()
    f2 = open(to_dir + '/' + name + '.txt', "w+")

    artist = f1[0].rstrip()

    i = 0
    old_time_delay = 0
    time_delay = 0
    for x in tqdm(f1[1:]):
        song_title, link = re.findall(r'^(.*) (http.*)$', x)[0] # separate song name and http (by re.findall)
        try:
            req = request.Request(
                url=link, 
                headers={'User-Agent': 'Mozilla/5.0'}
                )
            page = request.urlopen(req).read()
        except urllib.error.HTTPError:
            continue
        else:
            soup = BeautifulSoup(page, 'html.parser')
            lyrics = str(soup)
            song_title = re.findall(r'\w+$', x.split('.html')[0])[0]
            f2.write(str(i) + ', ' + artist + ', ' + song_title + ', ') 
            top_text = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
            bottom_text = '<!-- MxM banner -->'
            lyrics = lyrics.split(top_text)[1]
            lyrics = lyrics.split(bottom_text)[0]
            lyrics = lyrics.replace('<br>','').replace('</br>','').replace('</div>','').replace('<br/>','').strip()
            lyrics = re.sub(r'<i>.*</i>|,', ' ', lyrics)
            lyrics = re.sub(r'\n', '. ', lyrics.lstrip())
            f2.write(lyrics + '\n')
            while time_delay == old_time_delay:
                time_delay = random.uniform(5, 10)
            time.sleep(time_delay) # random delay ...
            i += 1
    f.close()
    f2.close()