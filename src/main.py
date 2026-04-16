"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"Printing {len(songs)} songs: \n")
    for s in songs:
        print(f"{s['title']} - Genre: {s['genre']}, Mood: {s['mood']}, Energy: {s['energy']}")
    
    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()

        def print_recommendations(recommendations: list) -> None:
            """Format and display recommendations in a clean, readable layout."""
            print("\n" + "="*70)
            print("TOP RECOMMENDATIONS".center(70))
            print("="*70 + "\n")
            
            for i, (song, score, explanation) in enumerate(recommendations, 1):
                print(f"{i}. {song['title']}")
                print(f"   Score: {score:.2f}/10")
                print(f"   Reason: {explanation}")
                print()
            
            print("="*70)
if __name__ == "__main__":
    main()
