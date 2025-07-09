import tkinter as tk
from user_interface import HangmanUI

def main():
    root = tk.Tk()          # Create main Tkinter window
    app = HangmanUI(root)   # Initialise UI
    root.mainloop()         # Keeps window open/responsive

# Only run game if this script is executed directly
if __name__ == "__main__":
    main()
