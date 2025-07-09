import tkinter as tk
from logic import mask_title, is_winner, is_loser
from omdb import get_random_movie
from PIL import Image, ImageTk, ImageFilter
import requests
from io import BytesIO

MAX_WRONG_GUESSES = 12

class HangmanUI:
    def __init__(self, root):
        # Initialise game
        self.root = root
        self.root.title("Hangman: Movie Edition")

        # Create container frame for  layout
        container = tk.Frame(root)
        container.pack(padx=10, pady=10)

        # Left frame (for poster)
        self.left_frame = tk.Frame(container)
        self.left_frame.pack(side=tk.LEFT, padx=10)

        # Right frame (for all other widgets)
        self.right_frame = tk.Frame(container)
        self.right_frame.pack(side=tk.LEFT, padx=10)

        # Poster in left frame
        self.poster_label = tk.Label(self.left_frame)
        self.poster_label.pack()

        # Word display in right frame
        self.label = tk.Label(self.right_frame, text="", font=("Courier", 24))
        self.label.pack(pady=10)

        # Info line
        self.info_label = tk.Label(self.right_frame, text="")
        self.info_label.pack()

        # Letter input field
        self.entry = tk.Entry(self.right_frame)
        self.entry.pack()

        # Guess button
        self.button = tk.Button(self.right_frame, text="Guess", command=self.guess_letter)
        self.button.pack(pady=10)

        # New game button
        self.reset_button = tk.Button(self.right_frame, text="New Game", command=self.start_new_game)
        self.reset_button.pack(pady=10)

        # Start first game
        self.start_new_game()
        self.update_display()

    def start_new_game(self):
        # Start new game with random movie
        self.entry.focus_set()
        self.movie_title, poster_url = get_random_movie()
        self.guessed = set()
        self.wrong_guesses = []

        # Reset interface
        self.info_label.config(text="")
        self.entry.config(state=tk.NORMAL)
        self.button.config(state=tk.NORMAL)

        # Load movie poster
        if poster_url:
            self.load_poster(poster_url)
        else:
            self.poster_label.config(image="")
            self.original_poster_img = None

        self.update_display()

    def load_poster(self, url):
        # Download and display movie poster
        try:
            response = requests.get(url, timeout=5)
            img_data = Image.open(BytesIO(response.content))
            self.original_poster_img = img_data.resize((150, 250)).convert('RGBA')
            self.update_poster_blur()
        except Exception as e:
            print(f"Failed to load poster: {e}")
            self.poster_label.config(image="")
            self.original_poster_img = None

    def update_poster_blur(self):
        # Decrease blur based on number of incorrect guesses
        print(f"Updating blur. Wrong guesses: {len(self.wrong_guesses)}")
        if not self.original_poster_img:
            return

        max_blur = MAX_WRONG_GUESSES - 2
        current_blur = max_blur - len(self.wrong_guesses)
        current_blur = max(current_blur, 0)
        print(f"Blur radius: {current_blur}")

        if current_blur > 0:
            blurred_img = self.original_poster_img.filter(ImageFilter.GaussianBlur(radius=current_blur))
        else:
            blurred_img = self.original_poster_img

        self.poster_img = ImageTk.PhotoImage(blurred_img)
        self.poster_label.config(image=self.poster_img)
        self.poster_label.image = self.poster_img

    def update_display(self):
        # Update info with current game state
        masked = mask_title(self.movie_title, self.guessed)
        self.label.config(text=masked)
        wrong_letters = ', '.join(self.wrong_guesses)
        attempts_left = MAX_WRONG_GUESSES - len(self.wrong_guesses)
        self.info_label.config(text=f"Wrong guesses: {wrong_letters} | Attempts left: {attempts_left}")

    def guess_letter(self):
        # Handle user input
        letter = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        # Check user has entered valid input (single letter)
        if not (letter.isalpha() and len(letter) == 1):
            self.info_label.config(text="Please enter a single alphabetic letter.")
            return

        # Handle user repeated guess
        if letter in self.guessed or letter in self.wrong_guesses:
            self.info_label.config(text=f"You already guessed '{letter}'. Try another letter.")
            return

        # Check if letter in movie title
        if letter in self.movie_title.lower():
            self.guessed.add(letter)
            print(f"Correct guess: {letter}")
        else:
            self.wrong_guesses.append(letter)
            print(f"Wrong guess: {letter} - total wrong: {len(self.wrong_guesses)}")

        # Update display and blur after guess
        self.update_display()
        self.update_poster_blur()

        # Win/lose condition
        if is_winner(self.movie_title, self.guessed):
            self.info_label.config(text="🎉 Congratulations! You won!")
            self.entry.config(state=tk.DISABLED)
            self.button.config(state=tk.DISABLED)
        elif is_loser(self.wrong_guesses, MAX_WRONG_GUESSES):
            self.info_label.config(text=f"You lost! The movie was: {self.movie_title}")
            self.entry.config(state=tk.DISABLED)
            self.button.config(state=tk.DISABLED)
