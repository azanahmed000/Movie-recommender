# 🎬 Movie Recommendation System (Streamlit + TMDB API)

A content-based movie recommender system built using TMDB metadata, cosine similarity, and a Streamlit web interface.  
The system recommends similar movies based on text vectorization and precomputed similarity.

This project was later **enhanced with Claude Sonnet 4.5**, which transformed the basic Streamlit UI into a more polished, animated, real-web-app-style experience with smooth transitions, better layout, and improved interaction flow.

---

## 🚀 Features

- Content-based recommendations using `CountVectorizer` / TF-IDF  
- Cosine similarity over vectorized metadata  
- Clean Streamlit UI with TMDB poster images  
- Precomputed artifacts:  
  - `movie.pkl` (movie dataframe)  
  - `simliarity.pkl` (similarity matrix)  
- TMDB API integration for real poster fetching  
- Enhanced frontend animations and UI effects via Claude Sonnet 4.5

---

## 📂 Project Structure

```
Movie_Recomendation_system.ipynb      # Preprocessing + similarity + pickle generation
streamlit web app.py                  # Streamlit frontend (UI + TMDB integration)
movie.pkl                             # Preprocessed movie dataframe
simliarity.pkl                        # Similarity matrix
tmdb_10k_movies.csv                   # TMDB metadata source
README.md
```

---

## 🧠 How It Works

### **1. Data Preparation (Notebook)**
- Load TMDB 10k CSV  
- Clean + merge relevant text columns  
- Construct a composite `tags` field  
- Vectorize using `CountVectorizer(max_features=10000, stop_words='english')`  
- Compute cosine similarity matrix  
- Save artifacts:
  ```
  pickle.dump(movies, open("movie.pkl", "wb"))
  pickle.dump(similarity, open("simliarity.pkl", "wb"))
  ```

---

### **2. Streamlit Web App**
The app:
- Loads `movie.pkl` + `simliarity.pkl`  
- Provides a movie dropdown selector  
- Computes top similar titles  
- Fetches real posters from TMDB API  
- Displays recommendations in a responsive grid  

Later, the UI was enhanced using **Claude Sonnet 4.5**, adding:
- Animated transitions  
- Smoother poster rendering  
- Better layout structure  
- More “Netflix-like” interaction  

---

## 🔑 TMDB API Key Setup

Create:

```
~/.streamlit/secrets.toml
```

Add:

```toml
TMDB_KEY = "c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
```

---

## ▶️ Running the App

### Install dependencies
```
pip install streamlit pandas numpy scikit-learn requests
```

### Run the Streamlit server

```
streamlit run "streamlit web app.py"
```

---


---

## 🏁 Summary

This repository demonstrates:
- A complete ML → vectorizer → similarity → inference pipeline  
- Integration with TMDB for real poster assets  
- A functional Streamlit interface  
- UI upgraded with Claude Sonnet 4.5 for a polished, animated, real-web experience  



