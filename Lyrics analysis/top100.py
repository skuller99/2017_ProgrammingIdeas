# -*- coding: utf-8 -*-
import os
import bs4
import re
import string
from collections import Counter
import requests
import urllib.request
import numpy as np
import pandas as pd

import sys
import codecs
#sys.stdout = codecs.getwriter('utf8')(sys.stdout)

os.chdir(r'C:\Svarbus reikalai\Python\IdeasLiberty\top100')

url = 'http://billboardtop100of.com/2015-2/'

# res = requests.get(url)
# res.raise_for_status()
# soup = bs4.BeautifulSoup(res.text,'lxml')

file = open("2015.txt", 'r')
soup = bs4.BeautifulSoup(file.read(),'lxml')
file.close()
entries = soup.select('tr td')

place = pd.Series((entries[i].text.strip() for i in range(0,len(entries),3)), name = 'Place')
place = pd.to_numeric(place)
artists = pd.Series((entries[i].text.strip() for i in range(1,len(entries),3)), name = 'Artists')
songs = pd.Series((entries[i].text.strip() for i in range(2,len(entries),3)), name = 'Songs')
songs = songs.str.split("\nLYRICS").str[0]


top = pd.concat([place,artists, songs], axis = 1)
top.set_index(['Artists','Songs'], inplace = True)
top['year'] = 2015

def words(text): # Suskaičiuoja žodžių skaičių tekste
	translator = str.maketrans({key: None for key in string.punctuation})
	return(Counter(text.lower().translate(translator).split()))
	
def lyrics (artist,song): #Ištraukia dainos žodžius
	res = requests.get('http://google.com/search?q=' + artist + " " + song + " azlyrics")
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text,'lxml')
	linkElems = soup.select('.r a')
	for i in range(len(linkElems)):
		if 'azlyrics' in linkElems[i].get('href'):
			link = linkElems[i].get('href')
			link = re.search(r'http.*html',link).group(0)
			
			#print(link)
			res = urllib.request.Request(link)
			resp = urllib.request.urlopen(res)
			respData = resp.read()
			soup = bs4.BeautifulSoup(respData,'lxml')
			textElems = soup.select('div')
			return words(textElems[22].text)

			
def addToTop(main, songCounter, artist, title): # Prideda dainą į lentelę
	percentage = pd.DataFrame([list(songCounter.values())])*100/sum(songCounter.values())
	percentage.columns = pd.Series(list(songCounter.keys())) # Naming columns by lyricss words
	percentage['Artists'] = artist
	percentage['Songs'] = title
	percentage.set_index(['Artists','Songs'], inplace = True)
	
	merge = main.combine_first(percentage)
	#print(merge.sort_values('Place').head())
	return merge.sort_values('Place')

	
#SongCounter = lyrics(top.index.values[1][0], top.index.values[1][1])

for i in range(len(top)):
	artist = top.index.values[i][0]
	title = top.index.values[i][1]
	print(artist)
	print(title)
	top = addToTop(top, lyrics(artist,title), artist,title)
print(top.head())
#print(addToTop(top, lyrics(top.index.values[1][0], top.index.values[1][1]), top.index.values[1][0], top.index.values[1][1]).head())

# file = open("words.txt", 'w')
# file.write(str(song))
# file.close()