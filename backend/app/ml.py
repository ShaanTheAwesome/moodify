# backend/app/ml.py

# ----------------------------
# Mood Analyzer (Rule-Based)
# ----------------------------

# Example genre/theme -> score mapping
# You can expand this later
GENRE_SCORE_MAP = {
    "pop": 7,
    "rock": 6,
    "rap": 5,
    "hip hop": 5,
    "classical": 6,
    "jazz": 7,
    "blues": 3,
    "metal": 4,
    "country": 6,
    "edm": 8,
    "sad": 2,
    "happy": 9,
    "energetic": 8,
    "calm": 6,
    # Add more as needed
}

# Mood ranges based on combined score
MOOD_RANGES = {
    "Sad/Depressed": (0, 3),
    "Neutral/Calm": (3, 6),
    "Happy/Energetic": (6, 10)
}


def map_genre_to_score(genre: str) -> float:
    """Maps a genre/theme to a numeric score. Defaults to 5 if unknown."""
    return GENRE_SCORE_MAP.get(genre.lower(), 5)


def compute_average_score(items: list) -> float:
    """Computes the average score of a list of genres/themes."""
    if not items:
        return 5  # neutral default
    scores = [map_genre_to_score(item) for item in items]
    return sum(scores) / len(scores)


def determine_mood(combined_score: float) -> str:
    """Determines the mood label from the combined score."""
    for mood, (low, high) in MOOD_RANGES.items():
        if low <= combined_score < high:
            return mood
    return "Neutral"


def analyze_mood(top_artists_genres: list, top_tracks_genres: list) -> dict:
    """
    Main function to analyze mood.
    
    Args:
        top_artists_genres: list of genres (strings) from top 15 artists
        top_tracks_genres: list of genres/themes (strings) from top 30 tracks
    
    Returns:
        dict containing artist_score, track_score, combined_score, mood_label
    """
    artist_score = compute_average_score(top_artists_genres)
    track_score = compute_average_score(top_tracks_genres)
    combined_score = (artist_score + track_score) / 2
    mood_label = determine_mood(combined_score)

    return {
        "artist_score": round(artist_score, 2),
        "track_score": round(track_score, 2),
        "combined_score": round(combined_score, 2),
        "mood": mood_label
    }
