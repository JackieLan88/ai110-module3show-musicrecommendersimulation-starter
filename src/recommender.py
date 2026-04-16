import csv
import math
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


# ---------------------------------------------------------------------------
# Feature vector helpers
# ---------------------------------------------------------------------------

TEMPO_MAX = 250.0  # normalizes tempo_bpm to [0, 1]


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """Return the cosine similarity between two numeric vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x ** 2 for x in a))
    norm_b = math.sqrt(sum(x ** 2 for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _build_song_vector(song: Dict, genres: List[str], moods: List[str]) -> List[float]:
    """Build a feature vector for a song dict: [genre_onehot | mood_onehot | numeric]."""
    genre_vec = [1.0 if song["genre"] == g else 0.0 for g in genres]
    mood_vec = [1.0 if song["mood"] == m else 0.0 for m in moods]
    numeric = [
        song["energy"],
        song["tempo_bpm"] / TEMPO_MAX,
        song["valence"],
        song["danceability"],
        song["acousticness"],
    ]
    return genre_vec + mood_vec + numeric


def _build_user_vector(user: Dict, genres: List[str], moods: List[str]) -> List[float]:
    """Build a feature vector for a user preference dict using the same layout as songs."""
    genre_vec = [1.0 if user.get("genre") == g else 0.0 for g in genres]
    mood_vec = [1.0 if user.get("mood") == m else 0.0 for m in moods]
    numeric = [
        user.get("energy", 0.5),
        user.get("tempo_bpm", 120.0) / TEMPO_MAX,
        user.get("valence", 0.5),
        user.get("danceability", 0.5),
        user.get("acousticness", 0.5),
    ]
    return genre_vec + mood_vec + numeric


def _explain(user: Dict, song: Dict) -> str:
    """Build a human-readable explanation of why a song was recommended."""
    reasons = []
    if song["genre"] == user.get("genre"):
        reasons.append(f"genre matches ({song['genre']})")
    if song["mood"] == user.get("mood"):
        reasons.append(f"mood matches ({song['mood']})")
    if "energy" in user and abs(song["energy"] - user["energy"]) <= 0.15:
        reasons.append(f"energy ({song['energy']:.2f}) is close to your target ({user['energy']:.2f})")
    if not reasons:
        reasons.append("overall audio features are a close match")
    return "Recommended because " + ", and ".join(reasons) + "."


# ---------------------------------------------------------------------------
# Functional API  (used by src/main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Uses: 2 points for genre match, 1 point for mood match,
    plus Gaussian scoring for numerical features.
    """
    score = 0.0
    reasons = []
    
    # Genre match: 2 points
    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"genre matches ({song['genre']}), 2 points")
    
    # Mood match: 1 point
    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"mood matches ({song['mood']}), 1 point")
    
    # Gaussian scoring for numerical features
    sigma = 0.15
    numerical_features = [
        ("energy", song["energy"], user_prefs.get("energy", 0.5)),
        ("tempo_bpm", song["tempo_bpm"] / TEMPO_MAX, user_prefs.get("tempo_bpm", 120.0) / TEMPO_MAX),
        ("valence", song["valence"], user_prefs.get("valence", 0.5)),
        ("danceability", song["danceability"], user_prefs.get("danceability", 0.5)),
        ("acousticness", song["acousticness"], user_prefs.get("acousticness", 0.5)),
    ]
    
    gaussian_score = 0.0
    for _, song_val, user_val in numerical_features:
        diff = abs(song_val - user_val)
        gaussian = math.exp(-(diff ** 2) / (2 * sigma ** 2))
        gaussian_score += gaussian
    
    score += gaussian_score
    
    if not reasons:
        reasons.append("overall audio features are a close match")
    
    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """
    Score every song against user_prefs using the score_song function.
    Returns a sorted list of (song, score, reasons) tuples.
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))
    
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]


# ---------------------------------------------------------------------------
# OOP API  (used by tests/test_recommender.py)
# ---------------------------------------------------------------------------

class Recommender:
    """OOP wrapper around the cosine similarity recommender."""

    def __init__(self, songs: List[Song]):
        """Initialize the recommender with a list of Song objects."""
        self.songs = songs
        self._genres = sorted({s.genre for s in songs})
        self._moods  = sorted({s.mood  for s in songs})

    def _song_to_dict(self, song: Song) -> Dict:
        """Convert a Song dataclass to a plain dict for vector building."""
        return {
            "genre": song.genre, "mood": song.mood,
            "energy": song.energy, "tempo_bpm": song.tempo_bpm,
            "valence": song.valence, "danceability": song.danceability,
            "acousticness": song.acousticness,
        }

    def _user_to_dict(self, user: UserProfile) -> Dict:
        """Convert a UserProfile dataclass to a plain dict for vector building."""
        return {
            "genre":       user.favorite_genre,
            "mood":        user.favorite_mood,
            "energy":      user.target_energy,
            "acousticness": 0.8 if user.likes_acoustic else 0.2,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs most similar to the user's profile via cosine similarity."""
        user_dict = self._user_to_dict(user)
        user_vec  = _build_user_vector(user_dict, self._genres, self._moods)

        scored = []
        for song in self.songs:
            song_vec = _build_song_vector(self._song_to_dict(song), self._genres, self._moods)
            scored.append((song, _cosine_similarity(user_vec, song_vec)))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-English explanation of why a song was recommended to a user."""
        return _explain(self._user_to_dict(user), self._song_to_dict(song))
