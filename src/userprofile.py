class UserProfile:
    """
    A class to store and manage a user's music preferences and target features.
    """

    AUDIO_FEATURE_RANGES = {
        "energy":        (0.0, 1.0),
        "tempo":         (40.0, 250.0),  # BPM
        "danceability":  (0.0, 1.0),
        "valence":       (0.0, 1.0),
        "acousticness":  (0.0, 1.0),
    }

    def __init__(self, user_id: str, name: str = ""):
        """
        Initialize a user profile.

        Args:
            user_id: Unique identifier for the user (cannot be empty)
            name: User's name (optional)
        """
        if not user_id:
            raise ValueError("user_id cannot be empty")
        self.user_id = user_id
        self.name = name
        self.favorite_genre: str | None = None
        self.favorite_mood: str | None = None
        self.audio_features: dict = {key: None for key in self.AUDIO_FEATURE_RANGES}

    def set_audio_features(self, features: dict) -> None:
        """
        Set multiple audio features at once.

        Args:
            features: Dictionary of audio feature names and their target values
        """
        unknown = set(features) - set(self.audio_features)
        if unknown:
            raise KeyError(f"Unknown features: {unknown}. Valid features: {list(self.audio_features)}")
        for name, value in features.items():
            self._validate_feature(name, value)
        self.audio_features.update(features)

    def set_audio_feature(self, feature_name: str, value: float) -> None:
        """
        Set a single audio feature.

        Args:
            feature_name: Name of the audio feature
            value: Target value for the feature
        """
        if feature_name not in self.audio_features:
            raise KeyError(f"Unknown feature '{feature_name}'. Valid features: {list(self.audio_features)}")
        self._validate_feature(feature_name, value)
        self.audio_features[feature_name] = value

    def _validate_feature(self, feature_name: str, value: float) -> None:
        min_val, max_val = self.AUDIO_FEATURE_RANGES[feature_name]
        if not (min_val <= value <= max_val):
            raise ValueError(
                f"'{feature_name}' must be between {min_val} and {max_val}, got {value}"
            )

    def get_audio_features(self) -> dict:
        """
        Retrieve all audio features.

        Returns:
            Copy of the audio features dictionary
        """
        return self.audio_features.copy()

    def __repr__(self) -> str:
        return (
            f"UserProfile(user_id={self.user_id}, name={self.name}, "
            f"genre={self.favorite_genre}, mood={self.favorite_mood}, "
            f"audio_features={self.audio_features})"
        )


if __name__ == "__main__":
    default_user = UserProfile(user_id="user1", name="User: Jackie")
    default_user.favorite_genre = "kpop"
    default_user.favorite_mood = "energetic"
    default_user.set_audio_features({
        "energy": 0.8,
        "tempo": 120,
        "danceability": 0.7,
        "valence": 0.6,
        "acousticness": 0.2,
    })
    print(default_user)
