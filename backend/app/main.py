from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from fastapi import Request
import urllib.parse
import os
import requests
import base64

# Loads API keys from .env so backend is ready to talk to Spotify
load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Creates backend server
app = FastAPI()

# Stores Spotify tokens
spotify_tokens = {}

# Frontend URIs
ORIGIN = "http://localhost:5173"
DASHBOARD = "http://localhost:5173/dashboard"


# Ensures browser doesn't block API due to cross-origin security
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Reusable functions
def get_access_token():
    token_data = spotify_tokens.get("curr_user")

    # No authorisation
    if not token_data:
        return None
    
    return token_data.get("access_token")

@app.get("/api/health")
def health():
    return {"status": "ok"}


"""
----------------------------------
User Authentication Functions
----------------------------------
"""
@app.get("/api/login")
def login():

    # Things I'm trying to retrieve
    scopes = [
        "user-read-private", "user-read-email", # Retrieves users profile
        "user-top-read",                        # Retrieves users top tracks
        "user-read-recently-played"             # Retrieves users recent tracks
    ]

    query_params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "scope": " ".join(scopes),
    }

    url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(query_params)

    return RedirectResponse(url)

@app.get("/api/callback")
def callback(request: Request):
    code = request.query_params.get("code")

    if not code:
        return {"error": "No code provided"}
    
    auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth_base64 = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI
    }

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers=headers,
        data=data
    )

    token_data = response.json()
    spotify_tokens["curr_user"] = token_data
    
    # return token_data
    return RedirectResponse(ORIGIN)

@app.get("/api/logout")
def logout():
    spotify_tokens.pop("curr_user", None)
    return RedirectResponse(ORIGIN)

# Returns True or False depending on whether user is authenticated
@app.get("/api/auth/status")
def auth_status():
    is_auth = "curr_user" in spotify_tokens
    return {"status": is_auth}

"""
----------------------------------
API Retrieval Functions
----------------------------------
"""

@app.get("/api/profile")
def get_me():
    access_token = get_access_token()
    if not access_token:
        return {"error": "not authenticated"}
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    profile = requests.get(
        "https://api.spotify.com/v1/me",
        headers=headers
    ).json()

    artists = requests.get(
        "https://api.spotify.com/v1/me/top/artists?limit=5",
        headers=headers
    ).json()
    
    tracks = requests.get(
        "https://api.spotify.com/v1/me/top/tracks?limit=5",
        headers=headers
    ).json()

    dashboard = {
        "profile": profile,
        "top_artists": artists,
        "top_tracks": tracks
    }

    return dashboard


# @app.get("/api/activity")
# def get_activity():
