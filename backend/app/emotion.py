# emotion.py
import math
from collections import Counter

# -----------------------------
# CONFIG / CONSTANTS
# -----------------------------

TEMPO_MIN = 60
TEMPO_MAX = 180

GENRE_LOUDNESS_BASELINE = {
    "edm": -4,
    "pop": -7,
    "dance pop": -6,
    "rock": -5,
    "alternative rock": -6,
    "metal": -4,
    "lo-fi": -15,
    "acoustic": -18,
    "classical": -20,
}

DEFAULT_LOUDNESS_BASELINE = -8

# -----------------------------
# NORMALIZATION HELPERS
# -----------------------------

def clamp(x, min_val=0.0, max_val=1.0):
    return max(min(x, max_val), min_val)

def normalize_tempo(tempo):
    return clamp((tempo - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN))

def normalize_loudness(loudness, baseline):
    # louder than baseline → positive intensity
    return clamp((loudness - baseline) / 10 + 0.5)

# -----------------------------
# CORE MODEL
# -----------------------------

def generate_mood(tracks, audio_features, artist_genres):
    if not audio_features:
        return {"error": "No audio features available"}

    n = len(audio_features)

    # ---- Aggregate raw features ----
    avg = lambda key: sum(f[key] for f in audio_features) / n

    avg_energy = avg("energy")
    avg_valence = avg("valence")
    avg_danceability = avg("danceability")
    avg_tempo = avg("tempo")
    avg_mode = avg("mode")

    # ---- Genre analysis ----
    genre_counts = Counter(artist_genres)
    top_genres = [g for g, _ in genre_counts.most_common(5)]

    baseline_loudness = DEFAULT_LOUDNESS_BASELINE
    for g in top_genres:
        if g in GENRE_LOUDNESS_BASELINE:
            baseline_loudness = GENRE_LOUDNESS_BASELINE[g]
            break

    avg_loudness = avg("loudness")
    loudness_norm = normalize_loudness(avg_loudness, baseline_loudness)
    tempo_norm = normalize_tempo(avg_tempo)

    # -----------------------------
    # EMOTION AXES (latent space)
    # -----------------------------

    arousal = clamp(
        0.45 * avg_energy +
        0.30 * tempo_norm +
        0.25 * loudness_norm
    )

    positivity = clamp(
        0.70 * avg_valence +
        0.30 * avg_mode
    )

    rhythm = avg_danceability

    intensity = clamp(
        0.6 * avg_energy +
        0.4 * loudness_norm
    )

    # -----------------------------
    # EMOTION SPACE MAPPING
    # -----------------------------

    if arousal > 0.7 and positivity > 0.6:
        emotion = "energetic / happy"
    elif arousal > 0.7 and positivity < 0.4:
        emotion = "angry / intense"
    elif arousal < 0.4 and positivity < 0.4:
        emotion = "sad / withdrawn"
    elif arousal < 0.4 and positivity > 0.6:
        emotion = "calm / content"
    else:
        emotion = "neutral / mixed"

    emotion_score = round((arousal + positivity) / 2, 2)

    # -----------------------------
    # CONFIDENCE ESTIMATION
    # -----------------------------

    def std(key):
        mean = avg(key)
        return math.sqrt(sum((f[key] - mean) ** 2 for f in audio_features) / n)

    volatility = (
        std("energy") +
        std("valence") +
        std("tempo") / TEMPO_MAX
    ) / 3

    confidence = clamp(1 - volatility)

    # -----------------------------
    # EXPLANATION
    # -----------------------------

    dominant_factors = sorted(
        {
            "energy": avg_energy,
            "valence": avg_valence,
            "tempo": tempo_norm,
            "danceability": avg_danceability,
            "loudness": loudness_norm
        }.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    # -----------------------------
    # FINAL OUTPUT
    # -----------------------------

    return {
        "emotion": emotion,
        "emotion_score": emotion_score,
        "confidence": round(confidence, 2),
        "emotion_axes": {
            "arousal": round(arousal, 2),
            "positivity": round(positivity, 2),
            "rhythm": round(rhythm, 2),
            "intensity": round(intensity, 2)
        },
        "dominant_factors": [f[0] for f in dominant_factors],
        "top_genres": top_genres
    }
