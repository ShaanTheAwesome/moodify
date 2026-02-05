# Moodify (Project Scrapped)

## Project Status
⚠️ **This project has been scrapped.**  

Moodify was intended to be a Spotify-based mood analysis application. The goal was to fetch a user's top tracks and their audio features from Spotify, then determine the user's current emotion based on these features.  

Unfortunately, due to **Spotify API limitations related to track availability by region**, the project could not be completed. Users from regions like Hong Kong could not access audio features for many tracks, since Spotify restricts track information to certain markets (e.g., IN, US, CA). This made it impossible to reliably retrieve the necessary data for mood analysis, even with thorough debugging and testing.  

---

## Project Overview
- **Backend:** Python, FastAPI  
- **Frontend:** React (planned for visualization of mood analysis)  
- **Spotify Integration:** Used Spotify Web API to fetch:
  - User top tracks (`/me/top/tracks`)
  - Audio features (`/audio-features`) — this part could not be fully implemented due to region restrictions

---

## Features Implemented
- User authentication with Spotify
- Fetching top tracks from the user's account
- Backend endpoints set up to return top tracks in JSON format
- Manual debugging scripts to retrieve audio features (unsuccessful due to API restrictions)

---

## Lessons Learned
Even though the project was scrapped, several technical skills and concepts were explored:
- Working with OAuth and Spotify Web API
- Handling requests in FastAPI and structuring endpoints
- Debugging API responses and handling HTTP status codes
- Understanding limitations imposed by external APIs and the importance of region restrictions

---

## Project Structure
```
.
├── backend
│   ├── main.py
│   ├── auth.py
│   ├── spotify.py
│   ├── utils.py
│   └── .env
├── frontend
│   ├── index.html
│   ├── script.js
│   └── styles.css
└── README.md
```

---

## References
- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
