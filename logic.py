def mask_title(title, guessed_letters):
    # Replace unguessed characters with underscore,
    # but leave non-alpha characters visible
    return ''.join(
        c if not c.isalpha() or c.lower() in guessed_letters else '_'
        for c in title
    )

def is_valid_guess(guess):
    # Check input is single alpha character
    return guess.isalpha() and len(guess) == 1

def is_winner(title, guessed_letters):
    # Return True if user guesses all characters in title
    return all(
        not c.isalpha() or c.lower() in guessed_letters
        for c in title
    )

def is_loser(wrong_guesses, max_attempts=12):
    # Return True if number of wrong guesses reaches or exceeds max attempts
    return len(wrong_guesses) >= max_attempts
