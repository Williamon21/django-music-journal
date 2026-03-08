import os
import base64
import requests
from django.conf import settings

TOKEN_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"


def get_spotify_token():
    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET

    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_b64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data, timeout=10)
    response.raise_for_status()
    return response.json()["access_token"]


def search_spotify_albums(query):
    token = get_spotify_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": query,
        "type": "album",
        "limit": 10,
    }

    response = requests.get(SEARCH_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    return response.json().get("albums", {}).get("items", [])


def search_spotify_tracks(query):
    token = get_spotify_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": query,
        "type": "track",
        "limit": 10,
    }

    response = requests.get(SEARCH_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    return response.json().get("tracks", {}).get("items", [])