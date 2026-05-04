import random   # Used for randomizing questions and answer choices
import json     # Used to load word data from a JSON file


# This function loads vocabulary data from an external file
def load_words():
    try:
        # Open the JSON file in read mode with proper encoding
        with open("words.json", "r", encoding="utf-8") as file:
            # Convert JSON data into a Python dictionary
            return json.load(file)
    
    # Handle case where file does not exist
    except FileNotFoundError:
        print("Error: words.json not found.")
    
    # Handle case where JSON format is invalid/corrupted
    except json.JSONDecodeError:
        print("Error: words.json is corrupted.")
    
    # Return empty dictionary if something fails (prevents crashes later)
    return {}
        

# Handles user input for selecting difficulty
def choose_difficulty(words):
    while True:  # Loop until valid input is given
        difficulty = input("Choose difficulty (easy/medium/hard): ").lower()
        
        # Check if input exists as a key in the words dictionary
        if difficulty in words:
            print(f"\nYou chose '{difficulty}' difficulty. Good luck!\n")
            return difficulty  # Return valid difficulty
        
        else:
            print("Invalid! Enter only (easy/medium/hard).")


# Handles one quiz question
def ask_question(word, correct, all_answers):
    print(f"\nWhat does '{word}' mean?\n")

    # Create a list of incorrect answers by excluding the correct one
    wrong_answers = [ans for ans in all_answers if ans != correct]

    # Limit number of wrong answers to max 3
    num_choices = min(3, len(wrong_answers))

    # Randomly pick wrong answers
    choices = random.sample(wrong_answers, num_choices)

    # Add correct answer to the list
    choices.append(correct)

    # Shuffle so correct answer is not always in same position
    random.shuffle(choices)

    # Fixed labels for multiple choice
    options = ["A", "B", "C", "D"]

    # Display answer choices
    for i in range(len(choices)):
        print(f"{options[i]}. {choices[i]}")

    # Input validation loop
    while True:
        user_choice = input("Your answer (A/B/C/D): ").upper()

        # Only allow valid options based on number of choices
        if user_choice in options[:len(choices)]:
            break
        else:
            print("Invalid! Enter only (A/B/C/D).")

    # Convert letter (A/B/C/D) into index
    index = options.index(user_choice)

    # Return True if correct, False if wrong
    return choices[index] == correct


# Saves results to a text file for tracking progress
def save_results(difficulty, score, total, percentage):
    with open("results.txt", "a") as file:  # "a" = append, keeps history
        file.write(f"Difficulty: {difficulty}\n")
        file.write(f"Score: {score}/{total}\n")
        file.write(f"Percentage: {percentage:.1f}%\n")
        file.write("-" * 30 + "\n")


# Tracks and updates the highest score achieved
def update_high_score(score):
    try:
        # Read existing high score
        with open("highscore.txt", "r") as file:
            high_score = int(file.read())
    
    # If file doesn't exist or is empty/invalid
    except (FileNotFoundError, ValueError):
        high_score = 0

    # If current score beats previous high score
    if score > high_score:
        with open("highscore.txt", "w") as file:  # overwrite old score
            file.write(str(score))
            print(f"🔥 New High Score: {score}")
    
    else:
        print(f"High Score: {high_score}")


# Load words once before game loop starts
words = load_words()

# Exit program if words failed to load
if not words:
    exit()


# Main game loop (allows replaying the game)
while True:
    
    print("\n=== Vocabulary Builder Game ===")

    # Get valid difficulty from user
    difficulty = choose_difficulty(words)

    score = 0
    lives = 3
    
    # Stores incorrectly answered questions for review
    wrong_questions = []

    # Get list of words for selected difficulty
    word_list = list(words[difficulty].keys())

    # Shuffle questions so order is different each game
    random.shuffle(word_list)

    # Loop through each word/question
    for i, word in enumerate(word_list, start=1):

        print(f"\nQuestion {i} of {len(word_list)}")
        print(f"Lives: {lives}")

        # Get correct answer for current word
        correct = words[difficulty][word]

        # Ask question and check result
        is_correct = ask_question(word, correct, words[difficulty].values())

        if is_correct:
            print("Correct!")
            score += 1
        
        else:
            print(f"Wrong! The correct answer is: {correct}")

            # Store mistake for later review
            wrong_questions.append((word, correct))

            lives -= 1
            print(f"Lives remaining: {lives}")

        # End game early if no lives left
        if lives == 0:
            print("\nGame over. You ran out of lives!")
            break

        print("-" * 30)


    # Display final results
    print(f"\nFinal score: {score} / {len(word_list)}")

    # Prevent division by zero
    percentage = (score / len(word_list) * 100) if word_list else 0

    print(f"\nPercentage: {percentage:.1f}%")

    # Update persistent high score
    update_high_score(score)

    # Save results to file
    save_results(difficulty, score, len(word_list), percentage)


    # Feedback based on performance
    if percentage == 100:
        print("Perfect! Your vocabulary is strong.")
    elif percentage >= 70:
        print("Good! Your vocabulary is decent.")
    elif percentage >= 40:
        print("Not bad! Keep improving.")
    else:
        print("Keep training your vocabulary. You'll get there!")


    # Review incorrect answers if any exist
    if wrong_questions:
        review = input("\nDo you want to review wrong answers? (yes/no): ").lower()

        if review == "yes":
            print("\n📘 Review your mistakes:")

            for word, correct in wrong_questions:
                print(f"- {word} → {correct}")

    else:
        print("\n🔥 No mistakes! Clean run.")


    # Replay loop
    while True:
        play_again = input("\nPlay again? (yes/no): ").lower()

        if play_again == "no":
            print("Thanks for playing!")
            exit()

        elif play_again == "yes":
            print("Let's start again!")
            break

        else:
            print("Invalid input!")
