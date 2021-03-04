#取得spotify上歌曲資料的相關套件
import pandas as pd
import numpy as np
import spotipy
import spotipy.util as util
import sys
from spotipy.oauth2 import SpotifyClientCredentials

# account information
user_id = 'q5wi1zj0t7tuwnx1j52u7sat5' #Spotify上帳號的ID
#Spotify  for Development的ID
client_id = 'c391b08e6b2e4ddf9bb1b6deca0ee2dc' 
client_secret = 'd6e1596ce9ec4ce1bcc02db48639a24e'
# authorization


token = util.prompt_for_user_token(user_id,
                                   'playlist-read-collaborative',
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri='http://127.0.0.1:1222'

                                   )
sp = spotipy.Spotify(auth=token)


# getting tracks in a playlist
playlist = sp.user_playlist(user_id, '37i9dQZF1DWTIcwQEMKk2L') # 要爬曲歌單的playlist ID
# 將playlist中每一首歌的資料(id,artist,name)解析出來
tracks_df = pd.DataFrame([(track['track']['id'],
                           track['track']['artists'][0]['name'],
                           track['track']['name'],                   
                          )
                          for track in playlist['tracks']['items']],
                             columns=['id', 'artist', 'name'] )
# 將playlist中所有歌曲的features分析出來
features = []
for n, chunk_series in tracks_df.groupby(np.arange(len(tracks_df)) // 50).id:
    features += sp.audio_features([*map(str, chunk_series)])
features_df = pd.DataFrame.from_dict(filter(None, features))
tracks_with_features_df = tracks_df.merge(features_df, on=['id'], how='inner')

# try getting many playlists at once 
'''
# sleep playlist 2992
a = 0
xx1 = np.array([]) 
xx2 = np.array([]) 
sleepPlaylist = ['37i9dQZF1DWTIcwQEMKk2L', '37i9dQZF1DWTlKxC5XMcbx', '37i9dQZF1DWZd79rJ6a7lp', 
'37i9dQZF1DX4sWSpwq3LiO', '37i9dQZF1DX0DxcHtn4Hwo', '37i9dQZF1DWVsXD88oyxvI', '37i9dQZF1DWX5zQ3IhNyvj',
'37i9dQZF1DX03b46zi3S82', '37i9dQZF1DX42o4SsMqqwn', '37i9dQZF1DX6mXxqnWLIPb', '37i9dQZF1DXcCnTAt8CfNe',
'37i9dQZF1DXbADqT0j1Cxt', '37i9dQZF1DXa1rZf8gLhyz', '37i9dQZF1DX8Sz1gsYZdwj', '37i9dQZF1DWV5BKo4w4oDg',
'37i9dQZF1DXbcPC6Vvqudd', '37i9dQZF1DXdJ5OFSzWeCS', '37i9dQZF1DWT0G9IZIf2WF', '37i9dQZF1DX8skPjZYk8mL', 
'37i9dQZF1DWUAeTOoyNaqm', '37i9dQZF1DX9if5QDLdzCa', '37i9dQZF1DXdbkmlag2h7b', '37i9dQZF1DWUKPeBypcpcP', 
'37i9dQZF1DX1n9whBbBKoL', '37i9dQZF1DWSiZVO2J6WeI', '37i9dQZF1DWXVDbSwjxsVN', '37i9dQZF1DXabJG3i5q2yk', 
'37i9dQZF1DX8gJ2FqE753V', '37i9dQZF1DWXzR2GKEiHgT', '37i9dQZF1DWXIrropGBmnR', '37i9dQZF1DWXjlftzHjTQ5', 
'37i9dQZF1DWVEt8B7a1H1M', '37i9dQZF1DX2mFmJUZg4Mp', '37i9dQZF1DX2y5WZJJL4SF', '37i9dQZF1DX4aYNO8X5RpR', 
'37i9dQZF1DWZhzMp90Opmn', '37i9dQZF1DWWtqHeytOZ8f', '37i9dQZF1DXbZmKskFbVct', '37i9dQZF1DX9QSrZ8cQbyd', 
'37i9dQZF1DX3WdioUzkg8I', '37i9dQZF1DWWSads6V2oIk', '37i9dQZF1DX8h3zQNo57xG', '37i9dQZF1DX0gdPaTnsXKL', 
'37i9dQZF1DX9NmDLwNQnXE', '37i9dQZF1DXb6LkIGouseT', '37i9dQZF1DX0ES2mnOVvai', '37i9dQZF1DWTSIF6WEosDG']


while a < len(sleepPlaylist):

	playlist = sp.user_playlist(user_id, sleepPlaylist[a])
	tracks_df = pd.DataFrame([(track['track']['id'],
                           track['track']['artists'][0]['name'],
                           track['track']['name'],                   
                          )
                          for track in playlist['tracks']['items']],
                             columns=['id', 'artist', 'name'] )
	features = []
	for n, chunk_series in tracks_df.groupby(np.arange(len(tracks_df)) // 50).id:
		features += sp.audio_features([*map(str, chunk_series)])
	features_df = pd.DataFrame.from_dict(filter(None, features))
	tracks_with_features_df = tracks_df.merge(features_df, on=['id'], how='inner')
	art = tracks_with_features_df.artist.values
	ener = tracks_with_features_df.energy.values
	art.shape = (len(tracks_with_features_df), 1)
	ener.shape = (len(tracks_with_features_df), 1)

	tem = tracks_with_features_df.tempo.values
	tem.shape = (len(tracks_with_features_df), 1)
	liv = tracks_with_features_df.liveness.values
	liv.shape = (len(tracks_with_features_df), 1)
	inst = tracks_with_features_df.instrumentalness.values
	inst.shape = (len(tracks_with_features_df), 1)	
	acou = tracks_with_features_df.acousticness.values
	acou.shape = (len(tracks_with_features_df), 1)
	spe = tracks_with_features_df.speechiness.values
	spe.shape = (len(tracks_with_features_df), 1)
	loud = tracks_with_features_df.loudness.values
	loud.shape = (len(tracks_with_features_df), 1)
	ener = tracks_with_features_df.energy.values
	ener.shape = (len(tracks_with_features_df), 1)
	dan = tracks_with_features_df.danceability.values
	dan.shape = (len(tracks_with_features_df), 1)

	if a == 0:
		xx1 = np.append(tem, liv, axis = 1)
		xx1 = np.append(xx1, inst, axis = 1)
		xx1 = np.append(xx1, acou, axis = 1)
		xx1 = np.append(xx1, spe, axis = 1)
		xx1 = np.append(xx1, loud, axis = 1)
		xx1 = np.append(xx1, ener, axis = 1)
		xx1 = np.append(xx1, dan, axis = 1)
	else:
		xx2 = np.append(tem, liv, axis = 1)
		xx2 = np.append(xx2, inst, axis = 1)
		xx2 = np.append(xx2, acou, axis = 1)
		xx2 = np.append(xx2, spe, axis = 1)
		xx2 = np.append(xx2, loud, axis = 1)
		xx2 = np.append(xx2, ener, axis = 1)
		xx2 = np.append(xx2, dan, axis = 1)

		xx1 = np.concatenate((xx1, xx2), axis=0)
	a+=1
print(len(xx1))
print(xx1)

import csv

with open('./sleep2992.csv', 'w', newline='') as csvfile:
	writer  = csv.writer(csvfile)
	writer.writerow(['tempo','liveness','instrumentalness','acousticness','speechiness',
		'loudness','energy','danceability'])
	for row in xx1:
		writer.writerow(row)

'''

# party playlist 2175
'''
a = 0
xx1 = np.array([]) 
xx2 = np.array([]) 
sleepPlaylist = ['37i9dQZF1DWZJRk0orDeVA', '37i9dQZF1DXaXB8fQg7xif', '37i9dQZF1DX71PXzGB2fd7', 
'37i9dQZF1DX71PXzGB2fd7', '37i9dQZF1DX4RDXswvP6Mj', '37i9dQZF1DXaveC2UHuytE', '37i9dQZF1DX6GwdWRQMQpq',
'37i9dQZF1DXcRXFNfZr7Tp', '37i9dQZF1DX1N5uK98ms5p', '37i9dQZF1DWY4xHQp97fN6', '37i9dQZF1DWVY4eLfA3XFQ',
'37i9dQZF1DX7F6T2n2fegs', '37i9dQZF1DX8a1tdzq5tbM', '37i9dQZF1DWUq3wF0JVtEy', '37i9dQZF1DX8FwnYE6PRvL',
'37i9dQZF1DXbS8bPVXXR2B', '37i9dQZF1DWXi7h4mmmkzD', '37i9dQZF1DXauOWFg72pbl', '37i9dQZF1DX1qioQ8EGhi8', 
'37i9dQZF1DX2W6AhhHuQN4', '37i9dQZF1DWYtQSOiZF6hj', '37i9dQZF1DXbNxO0uJPyJ9', '37i9dQZF1DXd1MXcE8WTXq', 
'37i9dQZF1DX3FNkD0kDpDV', '37i9dQZF1DX0011TOiJEnw', '37i9dQZF1DWV67mFOgnpbl', '37i9dQZF1DX0nBLMN0XzSQ', 
'37i9dQZF1DX0IlCGIUGBsA', '37i9dQZF1DX8Lj01u3MgX5', '37i9dQZF1DXdgnLr18vPvu', '37i9dQZF1DX2pto11EMGQc']


while a < len(sleepPlaylist):

	playlist = sp.user_playlist(user_id, sleepPlaylist[a])
	tracks_df = pd.DataFrame([(track['track']['id'],
                           track['track']['artists'][0]['name'],
                           track['track']['name'],                   
                          )
                          for track in playlist['tracks']['items']],
                             columns=['id', 'artist', 'name'] )
	features = []
	for n, chunk_series in tracks_df.groupby(np.arange(len(tracks_df)) // 50).id:
		features += sp.audio_features([*map(str, chunk_series)])
	features_df = pd.DataFrame.from_dict(filter(None, features))
	tracks_with_features_df = tracks_df.merge(features_df, on=['id'], how='inner')
	art = tracks_with_features_df.artist.values
	ener = tracks_with_features_df.energy.values
	art.shape = (len(tracks_with_features_df), 1)
	ener.shape = (len(tracks_with_features_df), 1)

	tem = tracks_with_features_df.tempo.values
	tem.shape = (len(tracks_with_features_df), 1)
	liv = tracks_with_features_df.liveness.values
	liv.shape = (len(tracks_with_features_df), 1)
	inst = tracks_with_features_df.instrumentalness.values
	inst.shape = (len(tracks_with_features_df), 1)	
	acou = tracks_with_features_df.acousticness.values
	acou.shape = (len(tracks_with_features_df), 1)
	spe = tracks_with_features_df.speechiness.values
	spe.shape = (len(tracks_with_features_df), 1)
	loud = tracks_with_features_df.loudness.values
	loud.shape = (len(tracks_with_features_df), 1)
	ener = tracks_with_features_df.energy.values
	ener.shape = (len(tracks_with_features_df), 1)
	dan = tracks_with_features_df.danceability.values
	dan.shape = (len(tracks_with_features_df), 1)

	if a == 0:
		xx1 = np.append(tem, liv, axis = 1)
		xx1 = np.append(xx1, inst, axis = 1)
		xx1 = np.append(xx1, acou, axis = 1)
		xx1 = np.append(xx1, spe, axis = 1)
		xx1 = np.append(xx1, loud, axis = 1)
		xx1 = np.append(xx1, ener, axis = 1)
		xx1 = np.append(xx1, dan, axis = 1)
	else:
		xx2 = np.append(tem, liv, axis = 1)
		xx2 = np.append(xx2, inst, axis = 1)
		xx2 = np.append(xx2, acou, axis = 1)
		xx2 = np.append(xx2, spe, axis = 1)
		xx2 = np.append(xx2, loud, axis = 1)
		xx2 = np.append(xx2, ener, axis = 1)
		xx2 = np.append(xx2, dan, axis = 1)

		xx1 = np.concatenate((xx1, xx2), axis=0)
	a+=1
print(len(xx1))
print(xx1)

import csv

with open('./party2175.csv', 'w', newline='') as csvfile:
	writer  = csv.writer(csvfile)
	writer.writerow(['tempo','liveness','instrumentalness','acousticness','speechiness',
		'loudness','energy','danceability'])
	for row in xx1:
		writer.writerow(row)
'''

# workout playlist 2175
a = 0
xx1 = np.array([]) 
xx2 = np.array([]) 
sleepPlaylist = ['37i9dQZF1DX3ZeFHRhhi7Y', '37i9dQZF1DX70RN3TfWWJh', '37i9dQZF1DXdxcBWuJkbcy', 
'37i9dQZF1DX76Wlfdnj7AP', '37i9dQZF1DXadOVCgGhS7j', '37i9dQZF1DWSJHnPb1f0X3', '37i9dQZF1DX9BXb6GsGCLl',
'37i9dQZF1DX32NsLKyzScr', '37i9dQZF1DX4eRPd9frC1m', '37i9dQZF1DWVhQ5d3I6DeF', '37i9dQZF1DWUVpAXiEPK8P',
'37i9dQZF1DWWPcvnOpPG3x', '37i9dQZF1DXe6bgV3TmZOL', '37i9dQZF1DWTl4y3vgJOXW', '37i9dQZF1DX0HRj9P7NxeE',
'37i9dQZF1DX7cmFV9rWM0u', '37i9dQZF1DX35oM5SPECmN', '37i9dQZF1DWSTc9FdySHtz', '37i9dQZF1DX0hWmn8d5pRe', 
'37i9dQZF1DWXmQEAjlxGhi', '37i9dQZF1DWZUTt0fNaCPB', '37i9dQZF1DWY3PJWG3ogmJ', '37i9dQZF1DXcCEH5EfTtzp', 
'37i9dQZF1DXbFRZSqP41al', '37i9dQZF1DWXx3Txis2L4x', '37i9dQZF1DWZYWNM3NfvzJ', '37i9dQZF1DXcYHCSWjSx6A', 
'37i9dQZF1DX5vVIxolcMKs']


while a < len(sleepPlaylist):

	playlist = sp.user_playlist(user_id, sleepPlaylist[a])
	tracks_df = pd.DataFrame([(track['track']['id'],
                           track['track']['artists'][0]['name'],
                           track['track']['name'],                   
                          )
                          for track in playlist['tracks']['items']],
                             columns=['id', 'artist', 'name'] )
	features = []
	for n, chunk_series in tracks_df.groupby(np.arange(len(tracks_df)) // 50).id:
		features += sp.audio_features([*map(str, chunk_series)])
	features_df = pd.DataFrame.from_dict(filter(None, features))
	tracks_with_features_df = tracks_df.merge(features_df, on=['id'], how='inner')
	art = tracks_with_features_df.artist.values
	ener = tracks_with_features_df.energy.values
	art.shape = (len(tracks_with_features_df), 1)
	ener.shape = (len(tracks_with_features_df), 1)

	tem = tracks_with_features_df.tempo.values
	tem.shape = (len(tracks_with_features_df), 1)
	liv = tracks_with_features_df.liveness.values
	liv.shape = (len(tracks_with_features_df), 1)
	inst = tracks_with_features_df.instrumentalness.values
	inst.shape = (len(tracks_with_features_df), 1)	
	acou = tracks_with_features_df.acousticness.values
	acou.shape = (len(tracks_with_features_df), 1)
	spe = tracks_with_features_df.speechiness.values
	spe.shape = (len(tracks_with_features_df), 1)
	loud = tracks_with_features_df.loudness.values
	loud.shape = (len(tracks_with_features_df), 1)
	ener = tracks_with_features_df.energy.values
	ener.shape = (len(tracks_with_features_df), 1)
	dan = tracks_with_features_df.danceability.values
	dan.shape = (len(tracks_with_features_df), 1)

	if a == 0:
		xx1 = np.append(tem, liv, axis = 1)
		xx1 = np.append(xx1, inst, axis = 1)
		xx1 = np.append(xx1, acou, axis = 1)
		xx1 = np.append(xx1, spe, axis = 1)
		xx1 = np.append(xx1, loud, axis = 1)
		xx1 = np.append(xx1, ener, axis = 1)
		xx1 = np.append(xx1, dan, axis = 1)
	else:
		xx2 = np.append(tem, liv, axis = 1)
		xx2 = np.append(xx2, inst, axis = 1)
		xx2 = np.append(xx2, acou, axis = 1)
		xx2 = np.append(xx2, spe, axis = 1)
		xx2 = np.append(xx2, loud, axis = 1)
		xx2 = np.append(xx2, ener, axis = 1)
		xx2 = np.append(xx2, dan, axis = 1)

		xx1 = np.concatenate((xx1, xx2), axis=0)
	a+=1
print(len(xx1))
print(xx1)

import csv

with open('./workout1904.csv', 'w', newline='') as csvfile:
	writer  = csv.writer(csvfile)
	writer.writerow(['tempo','liveness','instrumentalness','acousticness','speechiness',
		'loudness','energy','danceability'])
	for row in xx1:
		writer.writerow(row)









