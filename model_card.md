# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.  
Example: **MusRec 1.0**

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

Prompts:

- What kind of recommendations does it generate
- What assumptions does it make about the user
- Is this for real users or classroom exploration

MusRec 1.0 is a recommendation system that offers songs to users based on their style and/or preference. The recommendation for each song provided includes careful observation in key musical features (quantitative and categorical) and applying a score that could be compared with the user's preference.

This system is dedicated for users that have unique tastes in music and would like to also listen to new songs that are similar to their own preferred songs. It was also created for classroom exploration purposes.

---

## 3. How the Model Works

The model looks at genre, mood, energy, tempo, acousticness, danceability, and valence...a mix of numerical measurements and categories. The model takes in what genre, mood, and energy level a user prefers.

It compares each song's features against the user's preferences. Each feature gets a weight — energy is weighted more heavily (2.0) than genre (1.0), so songs that match the user's energy level matter more than genre matches. The higher the total weighted match, the higher the song's score, and the top scorers get recommended.

---

## 4. Data

Small but varied set of songs spanning several genres, including rock, jazz, and classical. Each song in the dataset is described using seven musical features: genre, mood, energy, tempo, acousticness, danceability, and valence. Additional songs were added.

---

## 5. Strengths

The system works best for users with clear, strong preferences — particularly those who like high-energy or very calm music. Because energy is weighted most heavily, the model does a good job of surfacing songs that match how intense or relaxed a user wants to feel while listening.

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

This systems includes all musical features (genre, mood, energy, tempo, accousticness, danceability, and valence), that are being utilized to score how similar a song from the dataset can be from one that is based on the user's preference. However, the dataset does not consist of multiples songs per genre, even though it does include at least one.

When applying a weight shift in musical features: energy and genre, out of three distinct user preferences, two of them still received accurate recommendations from the dataset based on the fact that energy is considered more valuable(2.0) to target than genre(1.0).

Given that energy is a quantitative measurable music feature, it also has limitations in how much is needed of energy (threshold) from each song. This constraint can cause an overfit since we are giving "energy" a high weight that the system uses to recommend us the best song that matches the user's preference.

In the dataset, most songs have an energy measured on the lower bounds( 0.22 - 0.44 ) and in the upper bounds (0.75–0.95). Only two songs can be considered in the middle of the "energy"-range (0.55–0.61). We can consider a potential bias if we have limited amount of songs we can offer for users or listeners who prefer moderate energy levels.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

### User profiles tested

- user 1 - preferences: {'genre': 'rock', 'mood': 'energetic', 'energy': 0.9}
- user 2 - preferences: {'genre': 'jazz', 'mood': 'relaxed', 'energy': 0.3}
- user 3 - preferences: {'genre': 'classical', 'mood': 'calm', 'energy': 0.2}

During each recommendation, I first observed the score that the system was calculating for each recommended song. Initially, genre was the feature that had the highest weight; I proceeded to compare how the songs would look if they didn't match the genre that the user preferred. I noticed, that genre did play a big role when scoring and that if it wouldn't have that assigned weight, the first songs recommended, weren't as competent than other songs features. It surprised me how large of an influence our decisions can be when you as the developer can assign any weight to crucial features that have the end-goal to provide accurate recommendations for others.

---

## 8. Future Work

Ideas for how you would improve the model next.

- Adding user-friendly UI
- Expand on music dataset to offer more diverse music for unique listeners
- Find different approaches to calculate a score
- Compare what music features could be removed

---

## 9. Personal Reflection

Building my first music recommendation system was an eye-opening experience, particularly seeing how minute fractional weights can so drastically shape the final output. This project deepened my appreciation for the mathematical foundations underlying these systems—specifically, how quantitative audio features are analyzed to align with user preferences. My biggest takeaway was understanding the distinction between various real-world recommendation methods and learning to break them down into core scoring and ranking rules.

With Claude's assistance, I successfully integrated the different components of the system, verifying that our dataset seamlessly connected to the recommender and that each track was accurately processed and evaluated against targeted feature profiles.
