# -*- coding: utf-8 -*-
"""
Created on Mon March 10 13:03:35 2021

Create playlists based on top songs of each artist on your discover weekly

@author: Connor C
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pp
from datetime import date
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
from dotenv import load_dotenv
import os

# Use your own spotify dev data below!
# set open_browser=False to prevent Spotipy from attempting to open the default browser, authenticate with credentials
scope = 'user-library-read user-library-modify playlist-modify-public ugc-image-upload'

#credentials loaded from .env
load_dotenv('.env')
client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")
redirect_uri = os.environ.get("redirect_uri")
discoweekuri = os.environ.get("discoweekuri")
discoartisturi = os.environ.get("discoartisturi")
usernamevar = os.environ.get("usernamevar")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope))
today = date.today()

toprint = "Discover More " + today.strftime("%m/%d")

def uploadimage(toprint,playlist):
    img = Image.new('RGB', (500, 500), color = (1, 1, 1))
    fnt = ImageFont.truetype('RobotoMono-Medium.ttf', 40)
    d = ImageDraw.Draw(img)
    d.text((20,20), toprint, font=fnt, fill=(255, 255, 255))

    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    sp.playlist_upload_cover_image(playlist,img_str) 

uploadimage(toprint,discoartisturi)

usedvalues = []

for track in sp.playlist_tracks(discoartisturi)["items"]:
    sp.playlist_remove_all_occurrences_of_items(discoartisturi,[track["track"]["uri"]])

for track_week in sp.playlist_tracks(discoweekuri)["items"]:
    oldsong = track_week["track"]["uri"]
    newsong = sp.artist_top_tracks(track_week["track"]["artists"][0]["uri"])["tracks"][0]["uri"]
    try:
        newsong2 = sp.artist_top_tracks(track_week["track"]["artists"][0]["uri"])["tracks"][1]["uri"]
    except:
        pass
    usedvalues.append(oldsong)
    sp.user_playlist_add_tracks(usernamevar, discoartisturi, [oldsong])
    if newsong not in usedvalues:
        sp.user_playlist_add_tracks(usernamevar, discoartisturi, [newsong])
        usedvalues.append(newsong)
    try:
        if newsong2 not in usedvalues:
            sp.user_playlist_add_tracks(usernamevar, discoartisturi, [newsong2])
            usedvalues.append(newsong2)
    except:
        pass