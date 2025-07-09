# 🎬 Movie-Themed Hangman  
This project is a movie-themed Hangman game built with Python and Tkinter. It fetches random movie titles and posters from the OMDb API, and gradually unblurs the poster as you make incorrect guesses.

---

## Features  
- Movie titles randomly fetched from the OMDb API  
- Poster starts blurred and sharpens with each wrong guess  
- 12 wrong guesses allowed before game over     

---

## How to Run  
1. Requires Python 3  
2. Install dependencies:
   pip install pillow requests
3. Run the game:
   python main.py

---

## File Overview  
- `main.py` — Entry point  
- `user_interface.py` — Tkinter-based UI logic  
- `logic.py` — Game logic and rules (e.g. win/loss detection)  
- `omdb.py` — Movie and poster fetching from OMDb API  
